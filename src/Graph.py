from collections import deque
from src.Node import Node

class Graph:

    def __init__(self):
        self.nodes = { }

    def get_node(self, id):
        if id not in self.nodes:
            self.nodes[id] = Node(id)

        return self.nodes[id]

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