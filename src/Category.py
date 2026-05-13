class Category:
    def __init__(self, id, name):
        self.nodes_id = {}
        self.__id = id
        self.__name = name
        self.__pagerank = 0

    def add_node(self, node):
        self.nodes_id[node.get_id()] = node

    def get_name(self):
        return self.__name

    def sumar_puntaje(self, p):
        self.__pagerank += p

    def get_len(self):
        return len(self.nodes_id)

    def get_pagerank(self):
        return self.__pagerank

    def __str__(self):
        return f"{self.__id}: {self.__name}"

    def __repr__(self):
        return f"{self.__id}: {self.__name}"