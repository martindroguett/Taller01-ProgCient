from collections import deque
from functools import reduce
from itertools import accumulate

from src.Node import Node
from src.Category import Category

class Graph:

    def __init__(self):
        self.nodes_id = { } #id: nodo
        self.names_id = { } #id: nombre
        self.cats = { } #id_cat: cat

    def get_node(self, id):
        """
        Busca un nodo en el diccionario del grafo, si no existe lo crea.
        :param id (int): id del nodo.
        :return: El nodo con el id.
        """

        if id not in self.nodes_id:
            self.nodes_id[id] = Node(id)

        return self.nodes_id[id]

    def get_cat(self, id):
        """
        Buscar una categoría en el diccionario del grafo.
        :param id (int): id de la categoría.
        :return: La categoría con el id si es que existe, de lo contrario None.
        """

        return self.cats.get(id, None)

    def get_ids_by_name(self, name):
        """
        Busca tod
        :param name:
        :return:
        """

        return self.names_id.get(name, set())

    def get_nodes(self):
        return self.nodes_id

    def set_name(self, node, name):
        node.set_name(name)

    def add(self,id_origin,name,id_dest):
        dest = self.get_node(id_dest)
        if dest.get_name() is None:
            self.set_name(dest,name)
            if name not in self.names_id:
                self.names_id[name] = set()

            self.names_id[name].add(id_dest)

        if id_origin != -1:
            origin = self.get_node(id_origin)
            origin.outcome_connect(id_dest)
            dest.income_connect(id_origin)

    #Categorias
    def count_nodes(self):
        return len(self.nodes_id)

    def count_edges(self):
        return reduce(lambda x, y: x + y.get_outcome_len(), self.nodes_id.values(), 0)

    def top_outcoming(self, places = 10):
        l = list(self.nodes_id.values())
        l.sort(key = lambda node: node.get_outcome_len(), reverse=True)
        return l[:places]

    def top_incoming(self, places = 10):
        l = list(self.nodes_id.values())
        l.sort(key=lambda node: node.get_income_len(), reverse=True)
        return l[:places]
    
    def summary(self):
        return {
            "articulos": self.count_nodes(),
            "enlaces": self.count_edges(),
        }

    def debug(self):
        if len(self.nodes_id) == 0:
            print("No hay nodes")

        for id, node in self.nodes_id.items():
            print(id, node)

    def bfs(self, start, end = None, print_bool = False):
        if start not in self.nodes_id:
            return

        parent = {start: None}

        if start == end:
            return [start]

        queue = deque([start])

        while queue:
            id = queue.popleft()

            if print_bool:
                print(self.nodes_id[id])

            for neighbor in self.nodes_id[id].get_outcome():
                if neighbor not in parent:
                    parent[neighbor] = id
                    queue.append(neighbor)

                    if end is not None and neighbor == end:
                        return self.path(parent, end)

        return "No hay camino"

    def path(self, parent, end):
        path = []
        curr = end

        while curr is not None:
            path.append(curr)
            curr = parent[curr]

        path.reverse()
        return path

    def dfs(self, start, print_bool = False):
        if start not in self.nodes_id:
            return

        stack = [start]

        visited = set()

        while stack:
            id = stack.pop()

            if print_bool:
                print(self.nodes_id[id])

            if id in visited:
                continue

            visited.add(id)

            for neighbor in self.nodes_id[id].get_outcome():
                if neighbor not in visited:
                    stack.append(neighbor)

    def pagerank(self, iteraciones = 20, d = 0.85):

        nodes = len(self.nodes_id)
        if nodes == 0:
            print("No hay nodos")
            return 0

        puntajes = {id: 1/nodes for id in self.nodes_id.keys()}

        for _ in range(iteraciones):

            puntajes_temp = {id: (1 - d)/nodes for id in self.nodes_id.keys()}

            extra = 0

            for id, n in self.nodes_id.items():
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

    def see_nodes(self, n = 10):
        id = 1
        while id <= len(self.nodes_id):

            for i in range(n):
                print(self.nodes_id.get(id, ""))
                id += 1

            yield

    def see_cats(self, n = 10):
        id = 1
        while id <= len(self.cats):

            for i in range(n):
                print(self.cats.get(id, ""))
                id += 1

            yield

    def bfs_cut_farness(self, id_start_node, threshold):
        """
        Computes the farness (sum of shortest paths) of a node
        using a BFS cut pruning approach.
        """
        # Initialize distances

        visited = {id_start_node}
        queue = deque([(id_start_node, 0)])

        total_distance = 0

        # Standard BFS
        while queue:
            current_node, dist = queue.popleft()

            for neighbor in self.get_node(current_node).get_outcome():
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_dist = dist + 1

                    total_distance += new_dist

                    if total_distance >= threshold:
                        return float('inf')

                    queue.append((neighbor, new_dist))

        # Closeness is 1 / farness
        if total_distance == 0:
            return float('inf')

        # Return farness; low farness = high closeness
        return total_distance