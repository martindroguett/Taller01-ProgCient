from collections import deque
from functools import reduce
from src.Node import Node

class Graph:

    def __init__(self):
        self.nodes = { }

    def get_node(self, id):
        if id not in self.nodes:
            self.nodes[id] = Node(id)

        return self.nodes[id]

    def get_nodes(self):
        return self.nodes

    def set_name(self, node, name):
            node.set_name(name)

    def add(self,id_origin,name,id_dest):
        dest = self.get_node(id_dest)
        if dest.get_name() is None:
            self.set_name(dest,name)

        if id_origin != -1:
            origin = self.get_node(id_origin)
            origin.outcome_connect(id_dest)
            dest.income_connect(id_origin)

    #Categories

    def count_nodes(self):
        return len(self.nodes)

    #def count_edges(self):
    #    return reduce(lambda x,y: x.getOutcoming() + y.getOutcoming(), self.nodes)
    def count_edges(self):
        return reduce(lambda x, y: x + y.get_outcome_len(), self.nodes.values(), 0) #MISMO CASO, SE CAMBIO A COMO ESTABA EN NODE


    """def top_outcoming(self, places = 10):
        l = list(self.nodes.values())
        l.sort(key = lambda node: node.getOutcoming())
        return l[:places]

    def top_incoming(self, places = 10):
        l = (list(self.nodes.values()))
        l.sort(key=lambda node: node.getIncoming())
        return l[-places:]"""

#EN AMBAS SE CAMBIARON LOS METODOS A COMO ESTABAN EN NODE. REVERSE PARA MAYOR A MENOR
    def top_outcoming(self, places = 10):
        l = list(self.nodes.values())
        l.sort(key = lambda node: node.get_outcome_len(), reverse=True)
        return l[:places]

    def top_incoming(self, places = 10):
        l = list(self.nodes.values())
        l.sort(key=lambda node: node.get_income_len(), reverse=True)
        return l[:places]
    
    def summary(self):
        return {
            "articulos": self.count_nodes(),
            "enlaces": self.count_edges(),
        }

    def debug(self):
        if len(self.nodes) == 0:
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

            if id in visited:
                continue

            print(id)

            visited.add(id)

            for neighbor in self.nodes[id].get_outcome():
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

    def pagerank(self, iteraciones = 20, d = 0.85):

        nodes = len(self.nodes)
        if nodes == 0:
            print("No hay nodos")
            return 0

        puntajes = {id: 1/nodes for id in self.nodes.keys()}

        for _ in range(iteraciones):

            puntajes_temp = {id: (1 - d)/nodes for id in self.nodes.keys()}

            extra = 0

            for id, n in self.nodes.items():
                if n.get_outcome_len() == 0:

                    extra += (puntajes[id] * d) / nodes

                    continue

                suma = d * (puntajes[id] / n.get_outcome_len())

                for i in n.get_outcome():
                    if i in puntajes_temp:
                        puntajes_temp[i] += suma

            if extra > 0:
                for id in puntajes_temp:
                    puntajes_temp[id] += extra

            puntajes = puntajes_temp

        return puntajes