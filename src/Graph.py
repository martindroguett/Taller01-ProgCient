from collections import deque
from functools import reduce
from src.Node import Node

class Graph:

    def __init__(self):
        self.nodes = { }

    def get_node(self, id):
        try:
            return self.nodes[id]

        except KeyError:
            self.__nodes[id] = Node(id)
            return self.__nodes[id]

    def setName(self, node, name):
            node.setName(name)

    def add(self,id_origin,name,id_dest):
        origin = self.get_node(id_origin)
        self.setName(origin,name)
        origin.outcomeConnect(id_dest)

        dest = self.get_node(id_dest)
        dest.incomeConnect(id_origin)

    def connect(self, origin, dest):
        origin.connect(dest)

    #Categories

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
        if (len(self.nodes) == 0):
            print("No hay nodes")

        for id, node in self.nodes.items():
            print(id, node)

    def bfs(self, start):
        if start not in self.nodes:
            return

        queue = deque([start])

        visited = set()

        while queue:
            id = queue.popleft()

            if (id in visited):
                continue

            print(id)

            visited.add(id)

            for neighbor in self.nodes[id].getLinks():
                if neighbor not in visited:
                    queue.append(neighbor)

    def dfs(self, start):
        if start not in self.nodes:
            return

        stack = [start]

        visited = set()

        while stack:
            id = stack.pop()

            if id in visited:
                continue

            print(id)

            visited.add(id)

            for neighbor in self.nodes[id].getLinks():
                if neighbor not in visited:
                    stack.append(neighbor)