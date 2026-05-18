import csv
import math

def cargar_CSV_grados(grafo):
    """
    Carga en dos archivos CSV los grados de entrada y salida, en orden descendente.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    datos = []
    for id, nodo in grafo.nodes_id.items():
        datos.append((id, nodo.name, nodo.get_outcome_len(), nodo.get_income_len()))

    with open("results/top_salidas.csv", "w", newline='', encoding="utf-8") as salida, open("results/top_entradas.csv", "w", newline='', encoding="utf-8") as entrada:

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

def cargar_CSV_pagerank(grafo, puntajes):
    """
    Carga en un archivo CSV la información de los nodos junto a su puntaje PageRank, en orden descendente según PR.

    Args:
        grafo (Graph): Grafo cargado con la información.
        puntajes (dict[int, float]): Puntajes PageRank de los nodos, según id.
    """

    with open("results/top_pagerank.csv", "w", newline='', encoding="utf-8") as archivo:
        writter = csv.writer(archivo)

        titulos = ["Posicion", "ID_Nodo", "Nombre_Articulo", "PageRank_Score", "Categorias"]
        writter.writerow(titulos)

        for pos, (id, p) in enumerate(puntajes):

            nodo_actual = grafo.get_node(id)
            nombre_articulo = nodo_actual.name

            cat_nodo = nodo_actual.categories

            if len(cat_nodo) > 0:
                for cat in cat_nodo:
                    cat.sumar_puntaje(p)

                texto_cat = ", ".join([cat.name for cat in cat_nodo])
            else:
                texto_cat = "sin categoria"

            fila_a_escribir = [pos, id, nombre_articulo, p, texto_cat]

            writter.writerow(fila_a_escribir)

def cargar_CSV_cat(grafo):
    """
    Carga en un archivo CSV la información de las categorías, además de su frecuencia y la tasa de puntaje según cantidad de nodos que pertenecen a ella.
    Ordenado de forma descendente según tasa.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    with open("results/top_categories.csv", "w", newline='', encoding="utf-8") as archivo:
        writter = csv.writer(archivo)

        titulos = ["Id", "Nombre", "Frecuencia", "PageRank_Score", "Tasa", "Tasa-Log"]
        writter.writerow(titulos)


        for id,cat in sorted(grafo.cats.items(), key = lambda x: x[1].pagerank/(x[1].get_len()+1), reverse=True):
            freq = cat.get_len()
            pr = cat.pagerank
            tasa = pr/(freq+1)
            writter.writerow([id, cat.name, freq, pr, tasa, tasa * math.log(freq+1)])

def cargar_CSV_filtrado_cat(grafo, cat_id):
    """
    Carga en dos archivos CSV la información de los nodos, y conexiones, que pertenecen a una categoría en específico.

    Args:
        grafo (Graph): Grafo cargado con la información.
        cat_id (int): Id de la categoría por la que se quiere filtrar.
    """

    cat = grafo.get_cat(cat_id)

    nombre_archivo_nodos = f"results/nodos_cat_{cat.name}.csv"
    nombre_archivo_edges = f"results/edges_cat_{cat.name}.csv"

    nodos = cat.nodes_id

    with open(nombre_archivo_nodos, "w", newline='', encoding="utf-8") as archivo_nodos, open(nombre_archivo_edges, "w", newline='', encoding="utf-8") as archivo_edges:
        writter_nodos = csv.writer(archivo_nodos)
        writter_edges = csv.writer(archivo_edges)

        titulos_nodos = ["Posicion", "Id", "Nombre_Articulo", "Categorias"]
        writter_nodos.writerow(titulos_nodos)

        titulos_edges = ["Source", "Target", "Type", "Weight"]
        writter_edges.writerow(titulos_edges)

        pos = 1

        for id, nodo in nodos.items():

            nodo = nodos[id]

            nombre_articulo = nodo.name
            cat_nodo = nodo.categories

            if len(cat_nodo) > 0:
                texto_cat = ", ".join([cat.name for cat in cat_nodo])
            else:
                texto_cat = "sin categoria"

            nodo_linea = [pos, id, nombre_articulo, texto_cat]
            writter_nodos.writerow(nodo_linea)

            pos += 1

            outcome = nodo.outcome

            for id_destino in outcome:

                if id_destino in nodos:
                    edge_linea = [id, id_destino, "Directed", 1]
                    writter_edges.writerow(edge_linea)

def cargar_CSV_closeness_centrality(resultados):
    """
    Carga en un archivo CSV la información de la cercanía de los nodos, en orden descendente según centralidad de salida.

    Args:
        dict: Diccionario donde las llaves son los ids originales de los nodos,
              y los valores son diccionarios con los nombres y resultados (centralidad,
              alcanzables, dist_media, conteo) separadas por "outbound" e "inbound".
    """

    ranking = sorted(resultados.items(), key=lambda x: x[1]['outbound']['centralidad'], reverse=True)

    with open("results/top_closeness.csv", "w", newline='', encoding="utf-8") as salida:

        writter_closeness = csv.writer(salida)

        titulos_salida = ["Id", "Nombre", "Out_centralidad", "Out_alcanzables", "Out_dist_media", "Out_conteo", "In_centralidad", "In_alcanzables",  "In_dist_media", "In_conteo"]

        writter_closeness.writerow(titulos_salida)

        for nid, r in ranking:
            writter_closeness.writerow([nid, r['nombre'], r['outbound']['centralidad'], r['outbound']['alcanzables'], r['outbound']['dist_media'], r['outbound']['conteo'], r['inbound']['centralidad'], r['inbound']['alcanzables'], r['inbound']['dist_media'], r['inbound']['conteo']])
