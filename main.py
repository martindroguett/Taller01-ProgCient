import csv
from src.WikiLoader import WikiLoader
from src.Spinner import Spinner
from collections import Counter
import time
import math
import numpy as np
from numba import njit
from typing import Tuple

def cargar_grafo():
    spinner = Spinner("Cargando wikiloader...")
    spinner.start()

    fileLoader = WikiLoader()
    grafo = fileLoader.cargar_grafo()
    spinner.stop()
    return grafo

def cargar_CSV_grados(grafo):

    spinner = Spinner("Cargando grados...")
    spinner.start()

    datos = []
    for id, nodo in grafo.nodes_id.items():
        datos.append((id, nodo.get_name(), nodo.get_outcome_len(), nodo.get_income_len()))

    with open("top_salidas.csv", "w", newline='', encoding="utf-8") as salida, open("top_entradas.csv", "w", newline='', encoding="utf-8") as entrada:

        writter_salida = csv.writer(salida)
        writter_entrada = csv.writer(entrada)

        titulos_salida = ["Id", "Nombre", "Grado_Salida"]
        titulos_entrada = ["Id", "Nombre", "Grado_Entrada"]

        writter_salida.writerow(titulos_salida)
        writter_entrada.writerow(titulos_entrada)

        datos.sort(key = lambda x: x[2], reverse = True)

        for id, nombre, s, _ in datos:
            writter_salida.writerow([id, nombre, s])

        datos.sort(key=lambda x: x[3], reverse=True)

        for id, nombre, _, e in datos:
            writter_entrada.writerow([id, nombre, e])

    spinner.stop()

def pagerank(grafo, top = 100, i = 20, d = 0.85):

    spinner = Spinner("Cargando puntajes pagerank...")
    spinner.start()

    puntajes = grafo.pagerank(i, d)

    if top == 0:
        spinner.stop()
        return sorted(puntajes.items(), key = lambda x: x[1], reverse = True)

    top_nodos = Counter(puntajes).most_common(top)

    spinner.stop()
    return top_nodos

def cargar_CSV_pagerank(grafo, puntajes):

    spinner = Spinner("Creando archivo CSV pagerank...")
    spinner.start()

    with open("top_pagerank.csv", "w", newline='', encoding="utf-8") as archivo:
        writter = csv.writer(archivo)

        titulos = ["Posicion", "ID_Nodo", "Nombre_Articulo", "PageRank_Score", "Categorias"]
        writter.writerow(titulos)

        for pos, (id, p) in enumerate(puntajes):

            nodo_actual = grafo.get_node(id)
            nombre_articulo = nodo_actual.get_name()

            cat_nodo = nodo_actual.get_categories()

            if len(cat_nodo) > 0:
                for cat in cat_nodo:
                    cat.sumar_puntaje(p)

                texto_cat = ", ".join([cat.get_name() for cat in cat_nodo])
            else:
                texto_cat = "sin categoria"

            fila_a_escribir = [pos, id, nombre_articulo, p, texto_cat]

            writter.writerow(fila_a_escribir)

    spinner.stop()

def cargar_CSV_filtrado_cat(grafo, cat_id):
    
    spinner = Spinner("Contando conexiones...")
    spinner.start()

    cat = grafo.get_cat(cat_id)

    nombre_archivo_nodos = f"nodos_cat_{cat.get_name()}.csv"
    nombre_archivo_edges = f"edges_cat_{cat.get_name()}.csv"

    nodos = cat.nodes_id
    
    with open(nombre_archivo_nodos, "w", newline='', encoding="utf-8") as archivo_nodos, open(nombre_archivo_edges, "w", newline='', encoding="utf-8") as archivo_edges:
        writter_nodos = csv.writer(archivo_nodos)
        writter_edges = csv.writer(archivo_edges)
    
        titulos_nodos = ["Posicion", "Id", "Nombre_Articulo", "Categorias"]
        writter_nodos.writerow(titulos_nodos)
    
        titulos_edges = ["Source","Target","Type","Weight"]
        writter_edges.writerow(titulos_edges)
    
        pos = 1
    
        for id, nodo in nodos.items():
    
            nodo = nodos[id]
    
            nombre_articulo = nodo.get_name()
            cat_nodo = nodo.get_categories()
    
            if len(cat_nodo) > 0:
                texto_cat = ", ".join([cat.get_name() for cat in cat_nodo])
            else:
                texto_cat = "sin categoria"
    
            nodo_linea = [pos, id, nombre_articulo, texto_cat]
            writter_nodos.writerow(nodo_linea)
    
            pos += 1
    
            outcome = nodo.get_outcome()
    
            for id_destino in outcome:
    
                if id_destino in nodos:
                    edge_linea = [id, id_destino, "Directed", 1]
                    writter_edges.writerow(edge_linea)
    
    spinner.stop()
    print("Archivos CSV creados")

def cargar_CSV_cat(grafo):
    spinner = Spinner("Creando archivo CSV categorias...")
    spinner.start()

    with open("top_categories.csv", "w", newline='', encoding="utf-8") as archivo:
        writter = csv.writer(archivo)

        titulos = ["Id", "Nombre", "Frecuencia", "PageRank_Score", "Tasa", "Tasa-Log"]
        writter.writerow(titulos)


        for id,cat in sorted(grafo.cats.items(), key = lambda x: x[1].get_pagerank()/(x[1].get_len()+1), reverse=True):
            freq = cat.get_len()
            pr = cat.get_pagerank()
            tasa = pr/(freq+1)
            writter.writerow([id, cat.get_name(), freq, pr, tasa, tasa * math.log(freq+1)])

    spinner.stop()

def resumen(grafo):
    resumen_final = grafo.summary()
    print("resumen final:", resumen_final)

def camino_corto(grafo, name1, name2):

    print(list(grafo.get_ids_by_name(name1)))
    print("-" * 20)
    print(list(grafo.get_ids_by_name(name2)))

    start = int(input("Start: "))
    end = int(input("End: "))

    spinner = Spinner("cargando BFS...")
    spinner.start()
    path = grafo.bfs(start, end)
    spinner.stop()

    for i in path:
        nodo = grafo.get_node(i)
        print(f"-> {nodo.get_name()} (id: {nodo.get_id()})")

def ver_nodos(grafo):
    jump = int(input("Introduce los nodos por pag: "))

    gen = grafo.see_nodes(jump)

    try:
        while True:
            next(gen)
            key = input("\nIngrese cualquier tecla para siguiente pagina (x para salir): ").lower()

            if (key == "x"):
                return

    except StopIteration:
        pass

def ver_cats(grafo):
    jump = int(input("Introduce las categorias por pag: "))

    gen = grafo.see_cats(jump)

    try:
        while True:
            next(gen)
            key = input("\nIngrese cualquier tecla para siguiente pagina (x para salir): ").lower()

            if (key == "x"):
                return

    except StopIteration:
        pass

def obtener_nodos_ordenados_por_grado(grafo):
    datos = []
    for id, nodo in grafo.nodes_id.items():
        datos.append((id, nodo.get_outcome_len()))
    return sorted(datos, key=lambda n: n[1], reverse=True)

def compilar_grafo_numpy(grafo: Graph) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list, dict]:
    print("[1/4] Convirtiendo diccionario de grafo a matrices CSR...")
    diccionario_grafo = grafo.get_nodes()
    n = len(diccionario_grafo)

    id_to_idx = {nid: i for i, nid in enumerate(diccionario_grafo.keys())}
    nombres = [""] * n

    out_deg = np.zeros(n, dtype=np.int32)
    in_deg  = np.zeros(n, dtype=np.int32)

    for nid, nodo in diccionario_grafo.items():
        u = id_to_idx[nid]
        nombres[u] = nodo.get_name()
        for out_id in nodo.get_outcome():
            if out_id in id_to_idx: out_deg[u] += 1
        for in_id in nodo.get_income():
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
        for out_id in nodo.get_outcome():
            if out_id in id_to_idx:
                out_indices[out_cursor[u]] = id_to_idx[out_id]
                out_cursor[u] += 1
        for in_id in nodo.get_income():
            if in_id in id_to_idx:
                in_indices[in_cursor[u]] = id_to_idx[in_id]
                in_cursor[u] += 1

    return out_indptr, out_indices, in_indptr, in_indices, nombres, id_to_idx

@njit
def bfs_pruned_numba(
    source: int, indptr: np.ndarray, indices: np.ndarray,
    count: np.ndarray, distsum: np.ndarray, T: np.ndarray, marked: np.ndarray,
    dist_buf: np.ndarray, queue_buf: np.ndarray, visited_buf: np.ndarray,
    k: int, t: int
):
    """Búsqueda en anchura ultrarrápida compilada a código máquina."""
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
def estimar_centralidad_core(n: int, indptr: np.ndarray, indices: np.ndarray, orden: np.ndarray, k: int):
    """Ejecuta el BFS sobre los k nodos de muestra seleccionados."""
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

def cargar_CSV_closeness(grafo, top_k_cercanias):

    spinner = Spinner("Creando archivo CSV closeness...")
    spinner.start()

    with open("top_closeness.csv", "w", newline='', encoding="utf-8") as archivo:
        writter = csv.writer(archivo)

        titulos = ["Posicion", "ID_Nodo", "Nombre_Articulo", "Closeness_Centrality","Categorias"]
        writter.writerow(titulos)

        for pos, (id, farness) in enumerate(top_k_cercanias, start = 1):

            closeness = 1 / farness

            nodo_actual = grafo.get_node(id)
            nombre_articulo = nodo_actual.get_name()
            cat_nodo = nodo_actual.get_categories()

            if len(cat_nodo) > 0:
                texto_cat = ", ".join([cat.get_name() for cat in cat_nodo])
            else:

                texto_cat = "sin categoria"

            fila_a_escribir = [pos, id, nombre_articulo, closeness, texto_cat]

            writter.writerow(fila_a_escribir)

    spinner.stop()

def estimar_centralidad(n: int, indptr: np.ndarray, indices: np.ndarray, k: int, semilla: int = 42):
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

def calcular_closeness_centrality_rapido(grafo, k):

    n = grafo.count_nodes()
    out_indptr, out_indices, in_indptr, in_indices, nombres, id_to_idx = compilar_grafo_numpy(grafo)

    print(f"[2/4] Calculando Centralidad SALIDA...")
    out_c, out_r, out_d, out_m = estimar_centralidad(n, in_indptr, in_indices, k)

    print(f"[3/4] Calculando Centralidad ENTRADA...")
    in_c, in_r, in_d, in_m = estimar_centralidad(n, out_indptr, out_indices, k)

    print("[4/4] Creando CSV...")
    resultados = {}
    for nid, i in id_to_idx.items():
        resultados[nid] = {
            "nombre": nombres[i],
            "outbound": {"centralidad": float(out_c[i]), "alcanzables": float(out_r[i])},
            "inbound": {"centralidad": float(in_c[i]), "alcanzables": float(in_r[i])},
        }
    return resultados

def cargar_CSV_closeness_centrality(resultados):
    ranking = sorted(resultados.items(), key=lambda x: x[1]['outbound']['centralidad'], reverse=True)
    spinner = Spinner("Cargando grados...")
    spinner.start()

    with open("top_closeness.csv", "w", newline='', encoding="utf-8") as salida:

        writter_closeness = csv.writer(salida)

        titulos_salida = ["Id", "Nombre", "Grado_Salida"]

        writter_closeness.writerow(titulos_salida)

        for nid, r in ranking:
            writter_closeness.writerow([nid, r['nombre'],r['outbound']['centralidad'] ])

    spinner.stop()

def menu():
    print("Taller 01: Prog. Cientifica")
    print("Por Martín Droguett, Francisco Romero y Lucas Munizaga.")
    print("Fecha: 15-05-2026")
    print("---------------------")
    grafo = cargar_grafo()

    option = 0

    print()

    while (option != 12):
        print("1. Cargar CSVs con informacion de grados de los nodos")
        print("2. Cargar CSV con Pageranks de cada nodo")
        print("3. Cargar CSV con informacion de categorias")
        print("4. Cargar CSV filtrando por categoria")
        print("5. Cargar CSV closeness (con sample k=100)")
        print("6. Obtener resumen del grafo")
        print("7. Obtener camino mas corto entre dos nodos")
        print("8. Hacer BFS desde un nodo origen")
        print("9. Hacer DFS desde un nodo origen")
        print("10. Ver informacion de nodos")
        print("11. Ver informacion de categorias")
        print("12. Salir")
        print("* Nota: Los archivos CSV se veran reflejados una vez termine el programa")
        option = int(input("> "))

        print()
        print("\033[H\033[J", end="")

        if option == 1:
            cargar_CSV_grados(grafo)

        elif option == 2:
            top = int(input("Ingrese los x primeros nodos (0 para todos): "))
            i = int(input("Iteraciones: "))
            d = float(input("Factor de amortiguación: "))

            puntajes = pagerank(grafo, top, i, d)
            cargar_CSV_pagerank(grafo, puntajes)

        elif option == 3:

            x = input("Atencion: Debe haberse seleccionado la opcion 2 antes (\"Si\" si lo hizo): ").lower()
            if (x == "si"):
                cargar_CSV_cat(grafo)

        elif option == 4:

            id = int(input("Introduce el id de la categoria: "))
            cargar_CSV_filtrado_cat(grafo, id)

        elif option == 5:
            resultados = calcular_closeness_centrality_rapido(grafo, k=100)
            cargar_CSV_closeness_centrality(resultados)

        elif option == 6:
            grafo.resumen()

        elif option == 7:
            name1 = input("Introduce el nombre del nodo origen: ") #Karl Marx
            name2 = input("Introduce el nombre del nodo destino: ") #Isabel Allende (politician)

            camino_corto(grafo, name1, name2)

        elif option == 8:
            id = int(input("Introduce el id del nodo origen: "))
            grafo.bfs(id, None, True)

        elif option == 9:
            id = int(input("Introduce el id del nodo origen: "))
            grafo.dfs(id, True)

        elif option == 10:
            ver_nodos(grafo)

        elif option == 11:
            ver_cats(grafo)

        elif option == 12:
            print("Saliendo...")

        else:
            print("--Opción inválida--")

        print()

if __name__ == "__main__":
    menu()
