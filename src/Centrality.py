import numpy as np
from numba import njit
from typing import Tuple, Optional
import time

# Asumiendo que Graph y WikiLoader están en tus archivos locales
from WikiLoader import WikiLoader
from Graph import Graph

# ─────────────────────────────────────────────
# 1. Compilación del Grafo a Arreglos CSR
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 2. BFS Podado (Compilado en C con Numba)
# ─────────────────────────────────────────────
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

    # Inicializar origen
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

    # Resetear el buffer de distancias solo para los visitados (O(visitados))
    for i in range(visited_count):
        dist_buf[visited_buf[i]] = np.inf

# ─────────────────────────────────────────────
# 3. Bucle Principal de Estimación (También en Numba)
# ─────────────────────────────────────────────
@njit
def estimar_centralidad_core(n: int, indptr: np.ndarray, indices: np.ndarray, orden: np.ndarray, k: int):
    """Ejecuta el BFS sobre los k nodos de muestra seleccionados."""
    count   = np.zeros(n, dtype=np.int32)
    distsum = np.zeros(n, dtype=np.float64)
    T       = np.zeros(n, dtype=np.int32)
    marked  = np.zeros(n, dtype=np.bool_)

    # Buffers pre-alojados para no reasignar memoria en cada BFS
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

def estimar_centralidad(n: int, indptr: np.ndarray, indices: np.ndarray, k: int, semilla: int = 42):
    np.random.seed(semilla)
    # Permutar Nodos para el muestreo aleatorio
    orden = np.random.permutation(n)
    
    # Llamar al core compilado
    count, distsum, T = estimar_centralidad_core(n, indptr, indices, orden, k)

    # Cálculos vectorizados finales (Vectorización rápida de NumPy)
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

# ─────────────────────────────────────────────
# 4. Orquestador
# ─────────────────────────────────────────────
def calcular_closeness_centrality_rapido(grafo: Graph, k: int = 100):
    n = grafo.count_nodes()
    
    out_indptr, out_indices, in_indptr, in_indices, nombres, id_to_idx = compilar_grafo_numpy(grafo)

    print(f"[2/4] Calculando Centralidad OUTBOUND (Numba JIT)...")
    start_time = time.time()
    out_c, out_r, out_d, out_m = estimar_centralidad(n, in_indptr, in_indices, k)
    print(f"      Outbound terminado en {time.time() - start_time:.2f} segundos.")

    print(f"[3/4] Calculando Centralidad INBOUND (Numba JIT)...")
    start_time = time.time()
    in_c, in_r, in_d, in_m = estimar_centralidad(n, out_indptr, out_indices, k)
    print(f"      Inbound terminado en {time.time() - start_time:.2f} segundos.")

    print("[4/4] Empaquetando resultados...")
    resultados = {}
    for nid, i in id_to_idx.items():
        resultados[nid] = {
            "nombre": nombres[i],
            "outbound": {"centralidad": float(out_c[i]), "alcanzables": float(out_r[i])},
            "inbound": {"centralidad": float(in_c[i]), "alcanzables": float(in_r[i])},
        }
    return resultados

# ─────────────────────────────────────────────
# Ejecución Principal
# ─────────────────────────────────────────────
if __name__ == "__main__":
    fileLoader = WikiLoader()
    
    print("Cargando grafo desde dataset...")
    t0 = time.time()
    grafo = fileLoader.cargar_grafo()
    print(f"Grafo cargado en {time.time() - t0:.2f} segundos. Nodos: {grafo.count_nodes()}, Aristas: {grafo.count_edges()}")

    # k=100 es ideal para equilibrar precisión y tiempo en 1.8M nodos
    resultados = calcular_closeness_centrality_rapido(grafo, k=100)
    
    # Imprimir un Top 5 rápido
    ranking = sorted(resultados.items(), key=lambda x: x[1]['outbound']['centralidad'], reverse=True)
    
    print("\n🏆 TOP 5 Nodos (Outbound Closeness):")
    for nid, r in ranking[:5]:
        print(f"[{nid}] {r['nombre']}: {r['outbound']['centralidad']:.6f}")