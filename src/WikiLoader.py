from pathlib import Path

from src.Graph import Graph
from src.Category import Category

class WikiLoader:
    def __init__(self):
        self.dir_dataset = Path().resolve() / "dataset"

    def cargar_nombres_categorias(self):
        ruta = self.dir_dataset / "wiki-topcats_Category_names.txt"
        categorias = {}

        with open(ruta,"r",encoding="utf-8") as file:
            for id,linea in enumerate(file, start=1):
                categorias[id] = Category(id, linea.strip())

        return categorias

    def cargar_nombres(self, ruta):
        with open(ruta,"r",encoding="utf-8") as file:
            for id,nombre in enumerate(file, start=1):
                if not nombre:
                    continue

                yield id,nombre.strip()

    def cargar_edges(self, ruta):
        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:
                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:

                    origin = int(partes[0])
                    dest = int(partes[1])

                    yield origin, dest

    def cargar_categorias(self, ruta):
        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:
                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:

                    cat = int(partes[1])
                    node = int(partes[0])

                    yield cat, node

    def cargar_grafo(self):

        rutaNombres = self.dir_dataset / "wiki-topcats_pagenames.txt"
        rutaNode = self.dir_dataset / "wiki-topcats.mtx"

        grafo = Graph()

        gen_nombres = self.cargar_nombres(rutaNombres)
        gen_edges = self.cargar_edges(rutaNode)

        try:
            id_nombre, nombre = next(gen_nombres)
            origin, dest = next(gen_edges)

            while True:
                if id_nombre == dest:
                    grafo.add(origin, nombre, dest)
                    origin, dest = next(gen_edges)

                else:
                    if id_nombre < dest:
                        grafo.add(-1, nombre, id_nombre)
                    id_nombre, nombre = next(gen_nombres)


        except StopIteration:
            pass

        grafo.cats = self.cargar_nombres_categorias()
        rutaCat = self.dir_dataset / "wiki-topcats_Categories.mtx"

        gen_cats = self.cargar_categorias(rutaCat)

        try:
            id_cat, id_node = next(gen_cats)

            while True:
                node = grafo.get_node(id_node)
                node.add_cat(grafo.cats[id_cat])

                grafo.cats[id_cat].add_node(node)
                id_cat, id_node = next(gen_cats)

        except StopIteration:
            pass

        return grafo