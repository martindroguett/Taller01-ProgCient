import csv
from src.WikiLoader import WikiLoader
from src.Spinner import Spinner
from collections import Counter
import time

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

        titulos = ["Id", "Nombre", "Frecuencia", "PageRank_Score"]
        writter.writerow(titulos)

        for id,cat in sorted(grafo.cats.items(), key = lambda x: x[1].get_pagerank(), reverse=True):
            writter.writerow([id, cat.get_name(), cat.get_len(), cat.get_pagerank()])

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

def top_k_cercanías(grafo, k):
    """
    Computes Top-K nodes based on closeness centrality using cut.
    """
    # Sort nodes by degree to improve pruning efficiency

    spinner = Spinner("Cargando cercanias...")
    spinner.start()

    print("Ordenando nodos por grado...")

    nodes_sorted = obtener_nodos_ordenados_por_grado(grafo)
    node_farness = []

    threshold = float('inf')
    total_nodos = len(nodes_sorted)

    print(f"Iniciando cálculo para {total_nodos} nodos con K={k}...")

    start_time_global = time.time()

    for i, (node_id, grado) in enumerate(nodes_sorted):

        start_node_time = time.time()

        farness = grafo.bfs_cut_farness(node_id, threshold)

        end_node_time = time.time()

        if farness != float('inf'):

            node_farness.append((farness, node_id))

            node_farness.sort(key=lambda x: x[0])

            if len(node_farness) > k:
                node_farness.pop()

            if len(node_farness) == k:
                threshold = node_farness[-1][0]

        if i <= k or i % 10000 == 0:
            tiempo_nodo = end_node_time - start_node_time
            tiempo_total = (time.time() - start_time_global) / 60
            print(f"[{i + 1}/{total_nodos}] Nodo {node_id} procesado en {tiempo_nodo:.4f}s | Threshold: {threshold} | Tiempo total: {tiempo_total:.2f} min")

    spinner.stop()

    return [(id,farness) for farness, id in node_farness]

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

def menu():
    print("Taller 01: Prog. Cientifica")

    grafo = cargar_grafo()

    option = 0

    print()

    while (option != 11):
        print("1. Cargar CSVs con informacion de grados de los nodos")
        print("2. Cargar CSV con Pageranks de cada nodo")
        print("3. Cargar CSV con informacion de categorias")
        print("4. Cargar CSV filtrando por categoria")
        print("5. Cargar CSV farness")
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

            cargar_CSV_pagerank(grafo, top, i, d)

        elif option == 3:
            cargar_CSV_cat(grafo)

        elif option == 4:

            id = int(input("Introduce el id de la categoria: "))
            cargar_CSV_filtrado_cat(grafo, id)

        elif option == 5:

            top = int(input("Ingrese los x primeros nodos (0 para todos): "))

            rank = top_k_cercanías(grafo, top)

            cargar_CSV_pagerank(grafo, rank)

        elif option == 6:
            grafo.resumen()

        elif option == 7:
            name1 = input("Introduce el nombre del nodo origen: ")
            name2 = input("Introduce el nombre del nodo destino: ")

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

        elif option == 12:
            cargar_CSV_closeness(grafo, top_k_cercanías(grafo, 100))

        print()

if __name__ == "__main__":
    menu()
