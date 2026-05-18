class Node:
    def __init__(self, id):
        self.__id = id
        self.__name = None
        self.__categories = set()
        self.__incoming_edges = set()
        self.__outcoming_edges = set()

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def add_cat(self,category):
        self.__categories.add(category)

    def get_name(self):
        return self.__name

    def get_outcome(self):
        return self.__outcoming_edges

    def get_categories(self):
        return self.__categories

    def income_connect(self,id):
        self.__incoming_edges.add(id)

    def outcome_connect(self,id):
        self.__outcoming_edges.add(id)

    def get_outcome_len(self):
        return len(self.__outcoming_edges)

    def get_income_len(self):
        return len(self.__incoming_edges)

    def __str__(self):
        return f"id: {self.__id}\nnombre: {self.__name}\ncategorias: {self.__categories}\nids entrada: {self.__incoming_edges}\nids salida: {self.__outcoming_edges}\n================================="