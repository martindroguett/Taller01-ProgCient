class Node:
    def __init__(self, id):
        self.__id = id
        self.__name = None
        self.__categories = set()
        self.__incomingEdges = set()
        self.__outcomingEdges = set()

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def add_cat(self,category):
        self.__categories.add(category)

    def get_name(self):
        return self.__name

    def get_outcome(self):
        return self.__outcomingEdges

    def income_connect(self,id):
        self.__incomingEdges.add(id)

    def outcome_connect(self,id):
        self.__outcomingEdges.add(id)

    def get_outcome_len(self):
        return len(self.__outcomingEdges)

    def get_income_len(self):
        return len(self.__incomingEdges)

    def __str__(self):
        return f" {self.__id} + {self.__name}  + {self.__categories}+incoming{self.__incomingEdges} + outcoming{self.__outcomingEdges}\n================================="