from src.Domain.Category import Category

class Node:
    """
    Clase que representa un nodo.
    Attributes:
        id (int): Id del nodo.
        name (str): Nombre del nodo.
        categories (set[Category]): Categorias del nodo.
        income (set[int]): Conexiones de entrada del nodo.
        outcome (set[int]): Conexiones de salida del nodo.

    """

    def __init__(self, id):
        self.id = id
        self.name = None
        self.categories = set()
        self.income = set()
        self.outcome = set()

    def add_cat(self,category):
        """
        Agrega una categoria al nodo.
        Args:
            category (Category): Categoria por agregar del nodo.
        """
        self.categories.add(category)

    def income_connect(self,id):
        """
        Conecta una entrada al nodo.

        Args:
            id(int): Id del nodo que conecta por entrada.
        """
        self.income.add(id)

    def outcome_connect(self,id):
        """
        Conecta una salida al nodo.

        Args:
            id(int): Id del nodo que conecta por salida.
        """
        self.outcome.add(id)

    def get_outcome_len(self):
        """
        Calcula la cantidad de conexiones de salida del nodo.

        Returns:
            int: Cantidad de conexiones de salida.
        """

        return len(self.outcome)

    def get_income_len(self):
        """
        Calcula la cantidad de conexiones de entrada del nodo.

        Returns:
            int: Cantidad de conexiones de entrada.
        """

        return len(self.income)

    def __str__(self):
        return f"id: {self.id}\nnombre: {self.name}\ncategorias: {self.categories}\nids entrada: {self.income}\nids salida: {self.outcome}\n================================="