from src.WikiLoader import WikiLoader
from src.Graph import Graph

fileLoader = WikiLoader()
grafo = fileLoader.cargar_grafo()

contador = 0
for id,node in grafo.nodes.items():
    print(node.__str__())
    if contador <20:
        contador+=1
    else:
        break
