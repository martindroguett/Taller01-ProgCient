class Node:
    def __init__(self, id):
        self.__id = id
        self.__nombre = None
        self.__lista_categorias = set()
        self.__lista_entradas = set()
        self.__lista_salidas = set()

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__nombre = name

    def add_cat(self,category):
        self.__lista_categorias.add(category)

    def get_name(self):
        return self.__nombre

    def get_outcome(self):
        return self.__lista_salidas

    def get_income(self):
        return self.__lista_entradas

    def get_categories(self):
        return self.__lista_categorias

    def income_connect(self,id):
        self.__lista_entradas.add(id)

    def outcome_connect(self,id):
        self.__lista_salidas.add(id)

    def get_outcome_len(self):
        return len(self.__lista_salidas)

    def get_income_len(self):
        return len(self.__lista_entradas)

    def __str__(self):
        return f"id: {self.__id}\nnombre: {self.__nombre}\ncategorias: {self.__lista_categorias}\nids entrada: {self.__lista_entradas}\nids salida: {self.__lista_salidas}\n================================="