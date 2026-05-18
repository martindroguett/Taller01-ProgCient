class Category:
    """
    Clase que representa una categoría.
    Attributes:
        nodes_id (dict[int, Node]): Diccionario con los nodos que pertenecen a la categoría, según id.
        id (int): Id de la categoría.
        name (str): Nombre de la categoría.
        pagerank (float): Puntaje acumulado de todos los nodos que pertenecen a la categoría.
    """

    def __init__(self, id, name):
        self.nodes_id = {}
        self.id = id
        self.name = name
        self.pagerank = 0

    def add_node(self, node):
        """
        Asigna un nodo a la categoría
        Args:
            node (Node): Nodo a agregar.
        """
        self.nodes_id[node.id] = node

    def sumar_puntaje(self, p):
        """
        Suma el puntaje ingresado al puntaje acumulado.

        Args:
            p (float): Puntaje por agregar.

        """
        self.pagerank += p

    def get_len(self):
        """
        Calcula la cantidad de nodos que pertenecen a la categoría.
        Returns:
            int: Cantidad de nodos que pertenecen a la categoría.
        """
        return len(self.nodes_id)

    def __str__(self):
        return f"{self.id}: {self.name}"

    def __repr__(self):
        return f"{self.id}: {self.name}"