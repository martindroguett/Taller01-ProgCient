class Node:
    def __init__(self, id):
        self.__id = id
        self.__name = None
        self.__links = {}  # Diccionario vacío que guardará claves de la forma: {id : Nodo}

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def getLinks(self):
        return self.__links

    def connect(self, dest):
        self.__links[dest.__id] = dest

    def __str__(self):
        return f" {hex(id(self))} + {self.__name} + {self.__links}"