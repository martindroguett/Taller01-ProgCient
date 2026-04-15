class Node:
    def __init__(self, id):
        self.__id = id
        self.__name = None
        self.__links = {}  # Diccionario vacío que guardará claves de la forma: {id : Nodo}
        self.__categories = set()
        self.__incomingEdges = set()
        self.__outcomingEdges = set()

    def setName(self, name):
        self.__name = name

    def add_cat(self,category):
        self.__categories.add(category)

    def getName(self):
        return self.__name

    def getLinks(self):
        return self.__outcomingEdges

    def connect(self, dest):
        self.__links[dest.__id] = dest

    def incomeConnect(self,id):
        self.__incomingEdges.add(id)

    def outcomeConnect(self,id):
        self.__outcomingEdges.add(id)   

    def __str__(self):

        return f" {self.__id} + {self.__name}  + {self.__categories}+incoming{self.__incomingEdges} + outcoming{self.__outcomingEdges}\n================================="