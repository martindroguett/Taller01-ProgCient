from collections import deque
from .Node import Node
from functools import reduce

class Graph:

    def __init__(self):
        self.__nodes = { }

    #Obtención
    def get_node(self, id):
        try:
            return self.__nodes[id]

        except KeyError:
            self.__nodes[id] = Node(id)
            return self.__nodes[id]

    #Agregación
    def add(self,id,name,edges):
        node = self.get_node(id)
        node.set_name(name)
#        for edge in edges:
            #nodo.outcomeConnect(edge)
            #nodo_salida = self.get_node(edge)
            #nodo_salida.incomeConnect(id)
    #Enlace
    def connect(self, origin, dest):
        origin.connect(dest)

    #Categories
    def load_categories(self,categories):
        for cat,ids in categories.items():
            for id in ids:
                self.__nodes[id].addCategory(cat)

    def count_nodes(self):
        return len(self.__nodes)

    def count_edges(self):
        return reduce(lambda x,y: x.getOutcoming() + y.getOutcoming(), self.__nodes)

    def top_outcoming(self, places = 10):
        l = list(self.__nodes.values())
        l.sort(key = lambda node: node.getOutcoming())
        return l[:places]

    def top_incoming(self, places = 10):
        l = (list(self.__nodes.values()))
        l.sort(key=lambda node: node.getIncoming())
        return l[:places]

    def summary(self):
        return {
            "articulos": self.count_nodes(),
            "enlaces": self.count_edges(),
        }

    def debug(self):
        if (len(self.__nodes) == 0):
            print("No hay nodes")

        for id, node in self.__nodes.items():
            print(id, node)

    def bfs(self, start):
        if (start not in self.__nodes):
            return

        queue = deque([start])

        visited = set([start])

        while queue:
            id = queue.popleft()

            print(id, self.get_node(id))

            for neighbor in self.__nodes[id].getLinks():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def dfs(self, start):
        if (start not in self.__nodes):
            return

        stack = [start]

        visited = set()

        while stack:
            id = stack.pop()

            if id in visited:
                continue

            print(id, self.get_node(id))
            visited.add(id)

            for neighbor in self.__nodes[id].getLinks():
                if neighbor not in visited:
                    stack.append(neighbor)