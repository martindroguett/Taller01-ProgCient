"""
Closeness Centrality para Grafos Dirigidos
Basado en: "Computing Classic Closeness Centrality, at Scale"
Cohen, Delling, Pajor, Werneck — COSN'14

Implementa el Algorithm 4 del paper:
  - Estima la centralidad de cercanía OUTBOUND para cada nodo v:
      B_out(v) = R_out(v) / S_out(v)
    donde S_out(v) = suma de distancias a nodos alcanzables desde v
          R_out(v) = cardinalidad del conjunto alcanzable desde v

  - Y la centralidad INBOUND (ejecutando el mismo algoritmo sobre G^T):
      B_in(v)  = R_in(v) / S_in(v)

Complejidad: O(k * (V + E) * log V)  — comparable a k Dijkstras completos.

Estructura esperada del grafo:
    grafo: dict[str, Nodo]
    class Nodo:
        id             : str
        nombre         : str
        lista_categorias: list
        lista_entradas : list[str]   # IDs de nodos que apuntan HACIA este nodo
        lista_salidas  : list[str]   # IDs de nodos a los que este nodo apunta
"""

import heapq
import random
from dataclasses import dataclass, field
from typing import Optional

from WikiLoader import WikiLoader


# ─────────────────────────────────────────────
# Clase Nodo de ejemplo (ajusta a la tuya)
# ─────────────────────────────────────────────
@dataclass
class Nodo:
    id: str
    nombre: str
    lista_categorias: list = field(default_factory=list)
    lista_entradas: list = field(default_factory=list)   # predecesores
    lista_salidas: list = field(default_factory=list)    # sucesores


# ─────────────────────────────────────────────
# Dijkstra con poda (pruned Dijkstra)
# ─────────────────────────────────────────────
def dijkstra_pruned(
    source_id: str,
    grafo: dict,
    neighbors_fn,          # función (nodo_id) -> lista de (vecino_id, peso)
    count: dict,
    k: int,
    distsum: dict,
    count_visits: dict,
    T: dict,
    t: int,
    marked: set,
) -> None:
    """
    Dijkstra podado desde source_id sobre el grafo indicado por neighbors_fn.
    Acumula en count[], distsum[] y T[] según el Algorithm 4 del paper.

    Parámetros
    ----------
    source_id    : nodo origen de esta búsqueda
    grafo        : dict[id, Nodo]
    neighbors_fn : (nodo_id) -> list[(vecino_id, peso)]
    count        : dict[id] -> int   — cuántos nodos del sample alcanzaron v
    k            : tamaño del sample (límite de poda)
    distsum      : dict[id] -> float — suma acumulada de distancias
    count_visits : dict[id] -> int   — alias de count (mismo objeto)
    T            : dict[id] -> int   — índice t en que count[v] llegó a k
    t            : índice de iteración actual (orden del nodo source)
    marked       : set de nodos ya procesados como source
    """
    dist = {source_id: 0.0}
    heap = [(0.0, source_id)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue

        if u == source_id:
            pass  # el nodo origen no se cuenta a sí mismo
        else:
            # Poda: si v ya tiene k nodos en su sample, no lo exploramos más
            if count[u] >= k:
                continue

            # Acumulamos
            distsum[u] += d
            count[u] += 1

            if count[u] == k:
                T[u] = t
                if u in marked:          # ya fue source → ajuste del paper
                    T[u] = t - 1

        if u not in grafo:
            continue

        for v_id, w in neighbors_fn(u):
            new_d = d + w
            if new_d < dist.get(v_id, float("inf")):
                # Poda anticipada: si v ya tiene k muestras, ignoramos
                if count.get(v_id, 0) >= k:
                    continue
                dist[v_id] = new_d
                heapq.heappush(heap, (new_d, v_id))


# ─────────────────────────────────────────────
# Funciones de vecindad
# ─────────────────────────────────────────────
def sucesores(nodo_id: str, grafo: dict, peso: float = 1.0):
    """Vecinos en el grafo original (aristas de salida)."""
    nodo = grafo.get(nodo_id)
    if nodo is None:
        return []
    return [(v_id, peso) for v_id in nodo.get_outcome() if v_id in grafo]


def predecesores(nodo_id: str, grafo: dict, peso: float = 1.0):
    """Vecinos en el grafo transpuesto G^T (aristas de entrada)."""
    nodo = grafo.get(nodo_id)
    if nodo is None:
        return []
    return [(v_id, peso) for v_id in nodo.get_income() if v_id in grafo]


# ─────────────────────────────────────────────
# Estimador de centralidad de cercanía (Algorithm 4)
# ─────────────────────────────────────────────
def estimar_centralidad(
    grafo: dict,
    k: int = 100,
    direccion: str = "outbound",   # "outbound" | "inbound"
    semilla: Optional[int] = None,
    peso_arista: float = 1.0,
) -> dict:
    """
    Estima la centralidad de cercanía (outbound o inbound) para todos los nodos
    usando el Algorithm 4 de Cohen et al. 2014.

    Retorna
    -------
    dict[nodo_id] -> {
        "centralidad": float,   # B(v) = R(v) / S(v), o 0 si no alcanza nada
        "alcanzables": float,   # R_hat(v): cardinalidad estimada del conjunto alcanzable
        "distancia_media": float,  # S(v)/R(v) = 1/B(v)
        "muestras": int,        # cuántos nodos del sample alcanzaron v
    }
    """
    if semilla is not None:
        random.seed(semilla)

    ids = list(grafo.keys())
    n = len(ids)

    if direccion == "outbound":
        # Corremos Dijkstra desde u sobre G^T (predecesores)
        # → estima quién puede llegar a v (inbound reach de v)
        # Paper Algorithm 4: "Perform pruned Dijkstra from u on G^T"
        # Esto acumula en distsum[v] la distancia dvu (de v a u) en G original.
        neighbors_fn = lambda nid: predecesores(nid, grafo, peso_arista)
    else:  # inbound
        # Corremos Dijkstra desde u sobre G (sucesores)
        neighbors_fn = lambda nid: sucesores(nid, grafo, peso_arista)

    # Inicialización
    count    = {nid: 0   for nid in ids}
    distsum  = {nid: 0.0 for nid in ids}
    T        = {nid: 0   for nid in ids}
    marked   = set()

    # Orden aleatorio de nodos (permutación uniforme)
    orden = ids[:]
    random.shuffle(orden)

    for t, u_id in enumerate(orden, start=1):
        marked.add(u_id)
        dijkstra_pruned(
            source_id=u_id,
            grafo=grafo,
            neighbors_fn=neighbors_fn,
            count=count,
            k=k,
            distsum=distsum,
            count_visits=count,
            T=T,
            t=t,
            marked=marked,
        )

    # ── Construir resultados ──────────────────────────────────────────────
    resultados = {}
    for nid in ids:
        c = count[nid]
        s = distsum[nid]

        if c == 0:
            # Nodo aislado (nadie lo alcanza / no alcanza a nadie)
            resultados[nid] = {
                "centralidad": 0.0,
                "alcanzables": 0.0,
                "distancia_media": float("inf"),
                "muestras": 0,
            }
            continue

        # Estimación de cardinalidad |R(v)|  (ecuación del paper)
        if c < k:
            r_hat = float(c)          # conteo exacto (alcanzó menos de k)
        else:
            # R_hat(v) = 1 + (k-1)(n-2) / (T[v] - 1)
            denom = T[nid] - 1
            if denom <= 0:
                r_hat = float(n - 1)
            else:
                r_hat = 1.0 + (k - 1) * (n - 2) / denom

        # Distancia media estimada
        dist_media = s / c            # promedio sobre las c muestras

        # B(v) = R(v) / S(v)  →  aproximado como  r_hat / (dist_media * r_hat)
        #      = 1 / dist_media
        # (la centralidad clásica de Bavelas es el inverso de la dist. media)
        centralidad = (1.0 / dist_media) if dist_media > 0 else 0.0

        resultados[nid] = {
            "centralidad": centralidad,
            "alcanzables": r_hat,
            "distancia_media": dist_media,
            "muestras": c,
        }

    return resultados


# ─────────────────────────────────────────────
# Función principal (outbound + inbound)
# ─────────────────────────────────────────────
def calcular_closeness_centrality(
    grafo,
    k: int = 100,
    semilla: Optional[int] = None,
) -> dict:
    """
    Calcula centralidad de cercanía outbound e inbound para grafos dirigidos.

    Parámetros
    ----------
    grafo   : dict[id, Nodo]
    k       : tamaño del sample (más alto = más preciso, más lento)
              Recomendado: k=100 para grafos grandes, k=50 para pruebas rápidas.
    semilla : semilla aleatoria para reproducibilidad

    Retorna
    -------
    dict[nodo_id] -> {
        "outbound": { centralidad, alcanzables, distancia_media, muestras },
        "inbound":  { centralidad, alcanzables, distancia_media, muestras },
        "nombre":   str,
    }
    """
    print(f"[closeness] Grafo: {grafo.count_nodes()} nodos | k={k}")

    print("[closeness] Calculando centralidad OUTBOUND...")
    out = estimar_centralidad(grafo.nodes_id, k=k, direccion="outbound", semilla=semilla)

    print("[closeness] Calculando centralidad INBOUND...")
    inn = estimar_centralidad(grafo.nodes_id, k=k, direccion="inbound", semilla=semilla)

    resultados = {}
    for nid, nodo in grafo.nodes_id.items():
        resultados[nid] = {
            "nombre": nodo.get_name(),
            "outbound": out[nid],
            "inbound":  inn[nid],
        }

    return resultados


# ─────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────
def top_nodos(resultados: dict, n: int = 10, metrica: str = "outbound") -> list:
    """
    Retorna los n nodos con mayor centralidad según 'outbound' o 'inbound'.

    Retorna lista de (nodo_id, nombre, centralidad) ordenada descendentemente.
    """
    ranking = [
        (nid, r["nombre"], r[metrica]["centralidad"])
        for nid, r in resultados.items()
    ]
    ranking.sort(key=lambda x: x[2], reverse=True)
    return ranking[:n]


def imprimir_ranking(resultados: dict, n: int = 10) -> None:
    print("\n" + "═" * 60)
    print(f"  TOP {n} — CENTRALIDAD OUTBOUND")
    print("═" * 60)
    for i, (nid, nombre, c) in enumerate(top_nodos(resultados, n, "outbound"), 1):
        print(f"  {i}. [{nid}] {nombre} {c}")

    print("\n" + "═" * 60)
    print(f"  TOP {n} — CENTRALIDAD INBOUND")
    print("═" * 60)
    for i, (nid, nombre, c) in enumerate(top_nodos(resultados, n, "inbound"), 1):
        print(f"  {i}. [{nid}] {nombre} {c}")
    print("═" * 60 + "\n")


# ─────────────────────────────────────────────
# Demo rápida con grafo de ejemplo
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # datos = {
    #     "A": ("Nodo Alpha",   [],         ["B", "C"]),
    #     "B": ("Nodo Beta",    ["A"],      ["D", "E"]),
    #     "C": ("Nodo Gamma",   ["A"],      ["E"]),
    #     "D": ("Nodo Delta",   ["B"],      ["F", "E"]),
    #     "E": ("Nodo Epsilon", ["B","C","D"], ["F"]),
    #     "F": ("Nodo Zeta",    ["D","E"],  []),
    # }
    # grafo: dict[str, Nodo] = {}
    # for nid, (nombre, entradas, salidas) in datos.items():
    #     grafo[nid] = Nodo(
    #         id=nid,
    #         nombre=nombre,
    #         lista_categorias=["demo"],
    #         lista_entradas=entradas,
    #         lista_salidas=salidas,
    #     )
    fileLoader = WikiLoader()
    grafo = fileLoader.cargar_grafo()
    # ── Ejecutar algoritmo ────────────────────────────────────────────────
    # k=6 aquí (grafo pequeño). En grafos grandes usa k=100.
    resultados = calcular_closeness_centrality(grafo, k=100, semilla=42)

    # ── Imprimir detalles ─────────────────────────────────────────────────
    print("\nDetalle por nodo:")
    print(f"{'ID':<4} {'Nombre':<15} {'CC-out':>10} {'CC-in':>10} "
          f"{'Alc-out':>10} {'Alc-in':>10}")
    print("-" * 65)
    for nid, r in resultados.items():
        print(
            f"{nid:<4} {r['nombre']} "
            f"{r['outbound']['centralidad']} "
            f"{r['inbound']['centralidad']} "
            f"{r['outbound']['alcanzables']} "
            f"{r['inbound']['alcanzables']}"
        )

    imprimir_ranking(resultados, n=6)