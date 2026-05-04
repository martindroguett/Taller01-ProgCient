import csv
from src.WikiLoader import WikiLoader
from src.Graph import Graph
from collections import Counter

"""fileLoader = WikiLoader()
grafo = fileLoader.cargar_grafo()

contador = 0
s = set()
duplicados = 0

for i in grafo.get_nodes():
    nombre = grafo.get_node(i).get_name()

    if nombre is None:
        print(f"El nodo {i} no tiene nombre")
    else:
        if nombre in s:
            print(f"Duplicado encontrado: {i} -> {nombre}")
            duplicados += 1
        else:
            s.add(nombre)

print("Nombres únicos:", len(s))
print("Total de duplicados:", duplicados)

print(len(grafo.get_nodes()))
print(len(s))



puntajes = grafo.pagerank()

top_20 = Counter(puntajes).most_common(20)

for id, v in top_20:
    print(id, grafo.get_node(id).get_name(), v)

"""

print("cargando wikiloader")
fileLoader = WikiLoader()
grafo = fileLoader.cargar_grafo()

print("cargando puntajes pagerank")
puntajes_obtenidos = grafo.pagerank()
top20_nodos = Counter(puntajes_obtenidos).most_common(20)

nombre_archivo = "datos_taller1.csv"
print("creando archivo")

with open(nombre_archivo, "w", newline='', encoding="utf-8") as archivo:
    writter = csv.writer(archivo)

    titulos = ["Posicion", "ID_Nodo", "Nombre_Articulo", "PageRank_Score", "Categorias"]
    writter.writerow(titulos)

    posicion_actual = 1

    for i in top20_nodos:
        id_nodo = i[0]
        puntaje_nodo = i[1]
        
        nodo_actual = grafo.get_node(id_nodo)
        nombre_articulo = nodo_actual.get_name()
        
        cat_nodo = nodo_actual.get_categories()
        
        texto_cat = ""

        if len(cat_nodo) > 0:
            texto_cat = " | ".join(cat_nodo)
        else:

            texto_cat = "sin categoria"

        puntaje_redondeado = round(puntaje_nodo, 6)

        fila_a_escribir = [posicion_actual, id_nodo, nombre_articulo, puntaje_redondeado, texto_cat]
        
        writter.writerow(fila_a_escribir)
        posicion_actual = posicion_actual + 1

print("\narchivo creado:", nombre_archivo)

resumen_final = grafo.summary()
print("resumen final:", resumen_final)