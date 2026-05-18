from src.Domain.Graph import Graph

import numpy as np
from numba import njit

def pagerank(grafo, iteraciones = 20, d = 0.85):
    """
    Calcula el PageRank de todos los nodos pertenecientes a un grafo.

    Args:
        grafo (Graph): Grafo donde se calcula el PageRank.
        iteraciones (int): Numero de iteraciones para calcular el PageRank.
        d (float): Amortiguacion o damping del PageRank, representa la probabilidad de un usuario de utilizar un hipervínculo.

    Returns:
         dict[int, float]: Diccionario con los puntajes de los nodos, según id.
    """
    nodes = len(grafo.nodes_id)

    puntajes = {id: 1 / nodes for id in grafo.nodes_id.keys()}

    for _ in range(iteraciones):

        puntajes_temp = {id: (1 - d) / nodes for id in grafo.nodes_id.keys()}

        extra = 0

        for id, n in grafo.nodes_id.items():
            if n.get_outcome_len() == 0:
                extra += (puntajes[id] * d) / nodes

                continue

            suma = d * (puntajes[id] / n.get_outcome_len())

            for i in n.outcome:
                if i in puntajes_temp:
                    puntajes_temp[i] += suma

        if extra > 0:
            for id in puntajes_temp:
                puntajes_temp[id] += extra

        puntajes = puntajes_temp

    return puntajes

def compilar_grafo_numpy(grafo):
    """
    Transforma el grafo a arreglos CSR (Compressed Sparse Row o vectores poco poblados)  de Numpy.
    Permite procesar el grafo a velocidades de C/C++ utilizando Numba.

    Args:
        grafo (Graph): Grafo original.
    Returns:
        out_indptr (ndarray): Lista de punteros. De esta forma los vecinos salientes del nodo i, en out_indices, se encuentran entre las posiciones out_indptr[i] hasta out_indptr[i+1]
        out_indices (ndarray): Destinos de las conexiones.
        in_indptr (ndarray): Lista de punteros. De esta forma los vecinos entrantes del nodo i, en in_indices, se encuentran entre las posiciones in_indptr[i] hasta in_indptr[i+1]
        in_indices (ndarray): Orígenes de las conexiones.
        nombres (list[str]): Lista con los nombres de los nodos.
        id_to_idx (dict): Mapeo del id original del nodo a su nuevo índice numérico (0 a N-1).
    """

    diccionario_grafo = grafo.nodes_id
    n = len(diccionario_grafo)

    id_to_idx = {nid: i for i, nid in enumerate(diccionario_grafo.keys())}
    nombres = [""] * n

    out_deg = np.zeros(n, dtype=np.int32)
    in_deg  = np.zeros(n, dtype=np.int32)

    for nid, nodo in diccionario_grafo.items():
        u = id_to_idx[nid]
        nombres[u] = nodo.name
        for out_id in nodo.outcome:
            if out_id in id_to_idx: out_deg[u] += 1
        for in_id in nodo.income:
            if in_id in id_to_idx: in_deg[u] += 1

    out_indptr = np.zeros(n + 1, dtype=np.int32)
    in_indptr  = np.zeros(n + 1, dtype=np.int32)
    out_indptr[1:] = np.cumsum(out_deg)
    in_indptr[1:]  = np.cumsum(in_deg)

    out_indices = np.empty(out_indptr[-1], dtype=np.int32)
    in_indices  = np.empty(in_indptr[-1],  dtype=np.int32)

    out_cursor = out_indptr[:-1].copy()
    in_cursor  = in_indptr[:-1].copy()

    for nid, nodo in diccionario_grafo.items():
        u = id_to_idx[nid]
        for out_id in nodo.outcome:
            if out_id in id_to_idx:
                out_indices[out_cursor[u]] = id_to_idx[out_id]
                out_cursor[u] += 1
        for in_id in nodo.income:
            if in_id in id_to_idx:
                in_indices[in_cursor[u]] = id_to_idx[in_id]
                in_cursor[u] += 1

    return out_indptr, out_indices, in_indptr, in_indices, nombres, id_to_idx

@njit
def bfs_pruned_numba(source, indptr, indices, count, distsum, T, marked, dist_buf, queue_buf, visited_buf, k, t):
    """
    Ejecuta un recorrido por anchura optimizado y podado usando Numba.
    Acumula las distancias para estimar la centralidad de cercanía.
    Utiliza @njit para mejorar el tiempo de ejecución.

    Args:
        source (int): Índice del nodo de origen para el recorrido.
        indptr (ndarray): Lista de punteros del formato CSR.
        indices (ndarray): Lista de vecinos del formato CSR.
        count (ndarray): Lista que cuenta cuántas veces ha sido alcanzado cada nodo.
        distsum (ndarray): Acumulador de la suma de distancias más cortas para cada nodo.
        T (ndarray): Arreglo que registra la iteración en la que un nodo alcanzó el límite 'k'.
        marked (ndarray): Máscara booleana de los nodos de origen seleccionados en la muestra.
        dist_buf (ndarray): Buffer temporal de distancias, utilizado para ahorrar memoria.
        queue_buf (ndarray): Buffer temporal que actúa como cola (queue) para el BFS.
        visited_buf (ndarray): Buffer para rastrear nodos visitados y limpiar dist_buf al final.
        k (int): Límite de veces que un nodo necesita ser alcanzado para detener su actualización.
        t (int): Número de la iteración actual.
    """

    head = 0
    tail = 0

    dist_buf[source] = 0.0
    queue_buf[tail] = source
    tail += 1

    visited_buf[0] = source
    visited_count = 1

    while head < tail:
        u = queue_buf[head]
        head += 1
        d = dist_buf[u]

        if u != source:
            if count[u] >= k:
                continue

            distsum[u] += d
            count[u] += 1

            if count[u] == k:
                T[u] = t
                if marked[u]:
                    T[u] = t - 1

        start = indptr[u]
        end = indptr[u + 1]

        for i in range(start, end):
            v = indices[i]

            if count[v] >= k:
                continue

            new_d = d + 1.0
            if new_d < dist_buf[v]:
                dist_buf[v] = new_d
                queue_buf[tail] = v
                tail += 1

                visited_buf[visited_count] = v
                visited_count += 1

    for i in range(visited_count):
        dist_buf[visited_buf[i]] = np.inf

@njit
def estimar_centralidad_core(n, indptr, indices, orden, k):
    """
    Ejecuta BFS sobre una muestra de nodos seleccionados para recolectar datos estadísticos.
    Utiliza Numba para su ejecución.

    Args:
        n (int): Cantidad total de nodos en el grafo.
        indptr (ndarray): Punteros CSR del grafo.
        indices (ndarray): Conexiones CSR del grafo.
        orden (ndarray): Arreglo con el orden aleatorio de los nodos (la muestra).
        k (int): Cantidad de nodos de muestra.

    Returns:
        count (ndarray): Lista que cuenta cuántas veces ha sido alcanzado cada nodo.
        distsum (ndarray): Acumulador de la suma de distancias más cortas para cada nodo.
        T (ndarray): Arreglo que registra la iteración en la que un nodo alcanzó el límite 'k'.
    """

    count   = np.zeros(n, dtype=np.int32)
    distsum = np.zeros(n, dtype=np.float64)
    T       = np.zeros(n, dtype=np.int32)
    marked  = np.zeros(n, dtype=np.bool_)

    dist_buf    = np.full(n, np.inf, dtype=np.float64)
    queue_buf   = np.zeros(n, dtype=np.int32)
    visited_buf = np.zeros(n, dtype=np.int32)

    for t_idx, u in enumerate(orden):
        marked[u] = True
        bfs_pruned_numba(
            u, indptr, indices,
            count, distsum, T, marked,
            dist_buf, queue_buf, visited_buf,
            k, t_idx + 1
        )

    return count, distsum, T

def estimar_centralidad(n, indptr, indices, k, semilla = 42):
    """
    Calcula la estimación estadística de la centralidad de cercanía y los nodos alcanzables, basado en un algoritmo de aproximación.

    Args:
        n (int): Cantidad total de nodos del grafo.
        indptr (ndarray): Punteros CSR del grafo.
        indices (ndarray): Conexiones CSR del grafo.
        k (int): Tamaño de la muestra.
        semilla (int): Semilla para la selección aleatoria de los nodos iniciales.

    Returns:
        centralidad (ndarray): El valor final estimado de la centralidad de cercanía.
        r_hat (ndarray): Estimación de la cantidad de nodos alcanzables desde y hacia el nodo.
        dist_media (ndarray): La distancia promedio a los nodos alcanzados.
        count (ndarray): Cantidad exacta de veces que el nodo fue descubierto en las "k" iteraciones.
    """

    np.random.seed(semilla)
    orden = np.random.permutation(n)

    count, distsum, T = estimar_centralidad_core(n, indptr, indices, orden, k)

    with np.errstate(divide='ignore', invalid='ignore'):
        dist_media = np.where(count > 0, distsum / count, np.inf)
        r_hat = np.empty(n, dtype=np.float64)

        mask_exact = count < k
        mask_estimado = ~mask_exact

        r_hat[mask_exact] = count[mask_exact].astype(np.float64)

        if mask_estimado.any():
            T_est = T[mask_estimado].astype(np.int64)
            denom = T_est - 1
            r_hat_est = np.where(denom > 0, 1.0 + (k - 1) * (n - 2) / denom, float(n - 1))
            r_hat[mask_estimado] = r_hat_est

        centralidad = np.where((dist_media > 0) & np.isfinite(dist_media), 1.0 / dist_media, 0.0)

    return centralidad, r_hat, dist_media, count

def calcular_closeness_centrality_rapido(grafo, k, spinner):
    """
    Función principal que coordina la conversión del grafo a NumPy y el cálculo  de la centralidad de cercanía estimada tanto de entrada (inbound) como de salida (outbound).

    Args:
        grafo (Graph): El grafo original.
        k (int): Tamaño de la muestra para los cálculos.
        spinner (Spinner): Objeto para mostrar el progreso en la consola.

    Returns:
        dict: Diccionario donde las llaves son los ids originales de los nodos,
              y los valores son diccionarios con los nombres y resultados (centralidad,
              alcanzables, dist_media, conteo) separadas por "outbound" e "inbound".
    """

    n = grafo.count_nodes()

    spinner.change_text("Convirtiendo grafo a matriz Numpy (1/4)...")
    out_indptr, out_indices, in_indptr, in_indices, nombres, id_to_idx = compilar_grafo_numpy(grafo)

    spinner.change_text("Calculando centralidad salida (2/4)...")
    out_c, out_r, out_d, out_m = estimar_centralidad(n, in_indptr, in_indices, k)

    spinner.change_text("Calculando centralidad entrada (3/4)...")
    in_c, in_r, in_d, in_m = estimar_centralidad(n, out_indptr, out_indices, k)

    resultados = {}
    for nid, i in id_to_idx.items():
        resultados[nid] = {
            "nombre": nombres[i],
            "outbound": {"centralidad": float(out_c[i]), "alcanzables": float(out_r[i]), "dist_media": float(out_d[i]), "conteo": float(out_m[i])},
            "inbound": {"centralidad": float(in_c[i]), "alcanzables": float(in_r[i]), "dist_media": float(in_d[i]), "conteo": float(in_m[i])},
        }
    return resultados
