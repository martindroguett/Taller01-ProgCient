from collections import deque
import Node

class Graph:

    def __init__(self):
        self.nodes = { }

    def get_node(self, id):
        if id not in self.nodes:
            self.nodes[id] = Node(id)

        return self.nodes[id]

    def setName(self, node, name):
            node.setName(name)

    def add(self,id,name,edges,categoria):
        nodo = self.get_node(id)
        self.setName(nodo,name)
        self.setCategory(nodo,categoria)

        for edge in edges:
            node =


    def connect(self, origin, dest):
        origin.connect(dest)

    def debug(self):
        if (len(self.nodes) == 0):
            print("No hay nodes")

        for id, node in self.nodes.items():
            print(id, node)

    def bfs(self, start):
        queue = []

        #size = len(self.nodes) Esto pasara cuando se pruebe todo o que se deba ingresar un nodo origen de donde comenzara el bfs
        size = 1791489
        visited = [False] * size

        #for i in range(size):

        #if not visited[i] and self.get_node(i).getName() is not None:
        queue.append(start)

        while queue:
            id = queue.pop(0)

            if (visited[id]):
                continue

            print(id, self.get_node(id))

            visited[id] = True

            for neighbor in self.nodes[id].getLinks():
                if not visited[neighbor]:
                    queue.append(neighbor)

    def dfs(self, start):
        stack = []

        size = 1791489
        visited = [False] * size

        stack.append(start)

        while stack:
            id = stack.pop()

            if (visited[id]):
                continue

            print(id, self.get_node(id))

            visited[id] = True

            for neighbor in self.nodes[id].getLinks():
                if not visited[neighbor]:
                    stack.append(neighbor)