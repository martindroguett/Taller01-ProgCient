class Node:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.links = {}  # Diccionario vacío que guardará claves de la forma: {id : Nodo}

    def setName(self, name):
        self.name = name

    def getLinks(self):
        return self.links

    def connect(self, key, dest):
        self.links[key] = dest