import csv
from src.WikiLoader import WikiLoader
from src.Spinner import Spinner
from collections import Counter

def cargar_grafo():
    spinner = Spinner("Cargando wikiloader...")
    spinner.start()

    fileLoader = WikiLoader()
    grafo = fileLoader.cargar_grafo()
    spinner.stop()
    return grafo

def grados(grafo):

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
    if (i != 20 and d != 0.85):
        i = int(input("Iteraciones: "))
        d = float(input("Factor de amortiguación: "))

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
                texto_cat = ", ".join(cat_nodo)
            else:

                texto_cat = "sin categoria"

            fila_a_escribir = [pos, id, nombre_articulo, p, texto_cat]

            writter.writerow(fila_a_escribir)

    spinner.stop()

def cargar_CSV_cat(cat):
    nombre_archivo_nodos = "nodos_taller1.csv"
    nombre_archivo_edges = "edges_taller1.csv"
    
    nodos = grafo.get_nodes()
    
    spinner = Spinner("Contando conexiones...")
    spinner.start()
    
    nodos_filtro = set([id for id,nodo in nodos.items() if cat in nodo.get_categories()])
    
    with open(nombre_archivo_nodos, "w", newline='', encoding="utf-8") as archivo_nodos, open(nombre_archivo_edges, "w", newline='', encoding="utf-8") as archivo_edges:
        writter_nodos = csv.writer(archivo_nodos)
        writter_edges = csv.writer(archivo_edges)
    
        titulos_nodos = ["Posicion", "Id", "Nombre_Articulo", "Categorias"]
        writter_nodos.writerow(titulos_nodos)
    
        titulos_edges = ["Source","Target","Type","Weight"]
        writter_edges.writerow(titulos_edges)
    
        pos = 1
    
        for id in nodos_filtro:
    
            nodo = nodos[id]
    
            nombre_articulo = nodo.get_name()
            cat_nodo = nodo.get_categories()
    
            if len(cat_nodo) > 0:
                texto_cat = ", ".join(cat_nodo)
            else:
                texto_cat = "sin categoria"
    
            nodo_linea = [pos, id, nombre_articulo, texto_cat]
            writter_nodos.writerow(nodo_linea)
    
            pos += 1
    
            outcome = nodo.get_outcome()
    
            for id_destino in outcome:
    
                if id_destino in nodos_filtro:
                    edge_linea = [id, id_destino, "Directed", 1]
                    writter_edges.writerow(edge_linea)
    
    spinner.stop()
    print("Archivos CSV creados")

def resumen(grafo):
    resumen_final = grafo.summary()
    print("resumen final:", resumen_final)

def bfs(grafo):

    print(list(grafo.get_ids_by_name("Patrioticheskaya Pesnya")))
    print("-" * 20)
    print(list(grafo.get_ids_by_name("Dyatlov Pass incident")))

    start = int(input("Start: "))
    end = int(input("End: "))

    spinner = Spinner("cargando BFS...")
    spinner.start()
    path = grafo.bfs(start, end)
    spinner.stop()

    for i in path:
        nodo = grafo.get_node(i)
        print(f"-> {nodo.get_name()} (id: {nodo.get_id()})")

grafo = cargar_grafo()
resumen(grafo)

grados(grafo)
cargar_CSV_pagerank(grafo, pagerank(grafo, 0))
