from collections import deque
from functools import reduce

from src.Domain.Node import Node
from src.Domain.Category import Category
class Graph:
    """
    Clase que representa un grafo dirigido, utilizando diccionarios para el almacenamiento de nodos y categorías.
    Attributes:
        nodes_id (dict[int, Node]): Diccionario con los nodos, según id.
        names_id (dict[int, str]): Diccionario con los nombres de los nodos, según id.
        cats (dict[int, Category]): Diccionario con las categorías, según id.
    """

    def __init__(self):
        self.nodes_id = { } #id: nodo
        self.names_id = { } #id: nombre
        self.cats = { } #id_cat: cat

    def get_node(self, id):
        """
        Busca un nodo en el diccionario del grafo, si no existe lo crea.
        Args:
            id (int): id del nodo.
        Returns:
             Node: El nodo con el id correspondiente.
        """

        if id not in self.nodes_id:
            self.nodes_id[id] = Node(id)

        return self.nodes_id[id]

    def get_cat(self, id):
        """
        Buscar una categoría en el diccionario del grafo.
        Args:
            id (int): id de la categoría.
        Returns:
            Category: La categoría con el id si es que existe, de lo contrario None.
        """

        return self.cats.get(id, None)

    def get_ids_by_name(self, name):
        """
        Busca todos aquellos nodos que tengan un nombre en específico.
        Args:
            name (string): Nombre del nodo.
        Returns:
            set[int]: Un set de las ids de los nodos que tengan el nombre correspondiente.
        """

        return self.names_id.get(name, set())

    def add(self,id_origin,name,id_dest):
        """
        Agrega conexiones entre nodos, además de asignar su nombre al nodo de destino.

        Args:
            id_origin (int): Id del nodo de origen.
            name (string): Nombre del nodo de destino.
            id_dest (int): Id del nodo de destino.
        """

        dest = self.get_node(id_dest)
        if dest.name is None:
            dest.name = name
            if name not in self.names_id:
                self.names_id[name] = set()

            self.names_id[name].add(id_dest)

        if id_origin != -1:
            origin = self.get_node(id_origin)
            origin.outcome_connect(id_dest)
            dest.income_connect(id_origin)

    def count_nodes(self):
        """
        Calcula el total de nodos en el grafo.
        Returns:
            int: Total de nodos en el grafo.
        """
        return len(self.nodes_id)

    def count_edges(self):
        """
        Calcula el total de aristas en el grafo.
        Returns:
            int: Total de aristas en el grafo.
        """
        return reduce(lambda x, y: x + y.get_outcome_len(), self.nodes_id.values(), 0)

    def summary(self):
        """
        Calcula un resumen del grafo, contando sus nodos y aristas.
        Returns:
            dict[str, int]: Diccionario con los nodos y aristas.
        """
        return {
            "articulos": self.count_nodes(),
            "enlaces": self.count_edges(),
        }

    def bfs(self, start, end = None, print_bool = False):
        """
        Realiza un recorrido del grafo por anchura. Puede encontrar el camino más corto entre dos nodos, o imprimir la información del nodo.

        Args:
            start (int): Id del nodo donde comienza el recorrido.
            end (int): Id del nodo donde termina el recorrido.
            print_bool (boolean): Booleano que determina si imprime o no la información del nodo.

        Returns:
            list[int]: Lista con las ids de los nodos en el camino entre start y end (inclusive).
        """

        if start not in self.nodes_id:
            return

        parent = {start: 0}

        if start == end:
            return [start]

        queue = deque([start])

        while queue:
            id = queue.popleft()

            if print_bool:
                print(self.nodes_id[id])

            for neighbor in self.nodes_id[id].outcome:
                if neighbor not in parent:
                    parent[neighbor] = id
                    queue.append(neighbor)

                    if end is not None and neighbor == end:
                        return self.path(parent, end)

        return []

    def path(self, parent, end):
        """
        Recorre los "padres" de los nodos, desde end, hasta encontrar el inicio del camino.

        Args:
            parent (dict[int, int]): Diccionario que almacena las ids de los nodos "hijos" junto a su "padre".
            end (int): Id del nodo donde termina el recorrido.

        Returns:
            list[int]: Lista con las ids de los nodos en el camino entre start y end (inclusive).
        """

        path = []
        curr = end

        while curr != 0:
            path.append(curr)
            curr = parent[curr]

        path.reverse()
        return path

    def dfs(self, start, print_bool = False):
        """
        Realiza un recorrido del grafo por profundidad. Puede imprimir la información del nodo.

        Args:
            start (int): Id del nodo donde comienza el recorrido.
            print_bool (boolean): Booleano que determina si imprime o no la información del nodo.
        """

        if start not in self.nodes_id:
            return

        stack = [start]

        visited = set()

        while stack:
            id = stack.pop()

            if id in visited:
                continue

            visited.add(id)

            if print_bool:
                print(self.nodes_id[id])

            for neighbor in self.nodes_id[id].outcome:
                if neighbor not in visited:
                    stack.append(neighbor)

    def see_nodes(self, n = 10):
        """
        Recorre e imprime todos los nodos del grafo, en intervalos de n.
        Args:
            n (int): Cantidad de nodos del grafo que recorre por intervalo.

        Returns:
            Generator[None]: Generador utilizado para esperar la siguiente iteración del recorrido.
        """

        id = 1
        while id <= len(self.nodes_id):

            for i in range(n):
                print(self.nodes_id.get(id, ""))
                id += 1

            yield

    def see_cats(self, n = 10):
        """
            Recorre e imprime todas las categorías del grafo, en intervalos de n.
            Args:
                n (int): Cantidad de catergorías del grafo que recorre por intervalo.

            Returns:
                Generator[None]: Generador utilizado para esperar la siguiente iteración del recorrido.
            """

        id = 1
        while id <= len(self.cats):

            for i in range(n):
                print(self.cats.get(id, ""))
                id += 1

            yield