from src.WikiLoader import WikiLoader
from src.Graph import Graph
from collections import Counter

fileLoader = WikiLoader()
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

"""

puntajes = grafo.pagerank()

top_20 = Counter(puntajes).most_common(20)

for id, v in top_20:
    print(id, grafo.get_node(id).get_name(), v)

"""