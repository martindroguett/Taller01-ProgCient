class ArticuloWikipedia:
    """Modela un articulo de Wikipedia con categorias y enlaces asociados."""

    def __init__(self, id_articulo, nombre):
        self.id_articulo = id_articulo
        self.nombre = nombre
        self.categorias = set()
        self.enlaces_salida = set()
        self.enlaces_entrada = set()

    def agregar_categoria(self, categoria):
        self.categorias.add(categoria)

    def agregar_enlace_salida(self, id_destino):
        self.enlaces_salida.add(id_destino)

    def agregar_enlace_entrada(self, id_origen):
        pass
        # TODO

    def grado_salida(self):
        pass
        # TODO

    def grado_entrada(self):
        pass
        # TODO

    def __str__(self):
        return f"{self.id_articulo} - {self.nombre}"
