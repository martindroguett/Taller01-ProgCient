from pathlib import Path

from src.Graph import Graph
class WikiLoader:
    def __init__(self):
        self.dir_dataset = Path().resolve() / "dataset"
    
    def __cargar_nombres_categorías(self):
        ruta = self.dir_dataset / "wiki-topcats-Category_names.txt"
        categorias = {}
        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:

                if not linea or ";" not in linea:
                    continue

                parte_categoria,ids = linea.strip().split(";")
                nombre_categoria = parte_categoria.replace("Category:","").strip()
                
                ids = ids.lstrip().rstrip().split(" ")

                categorias[nombre_categoria] = set()

                for id in ids:
                    if not id: 
                        break
                    categorias[nombre_categoria].add(id)
        return categorias

    def cargar_nombres_categorias(self):
        ruta = self.dir_dataset / "wiki-topcats_Category_names.txt"
        categorias = {}

        with open(ruta,"r",encoding="utf-8") as file:
            for idx,linea in enumerate(file, start=1):
                categorias[idx] = linea.strip()

        return categorias

    def cargar_nombres(self, ruta):
        with open(ruta,"r",encoding="utf-8") as file:
            for id,nombre in enumerate(file, start=1):
                if not nombre:
                    continue

                yield id,nombre

    def cargar_edges(self, ruta):
        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:
                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:

                    origin = int(partes[1])
                    dest = int(partes[0])

                    yield dest, origin

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
            dest, origin = next(gen_edges)

            while True:
                if id_nombre == origin:
                    grafo.add(origin, nombre, dest)
                    dest, origin = next(gen_edges)

                else:
                    id_nombre, nombre = next(gen_nombres)

        except StopIteration:
            pass

        categorias = self.cargar_nombres_categorias()
        rutaCat = self.dir_dataset / "wiki-topcats_Categories.mtx"

        gen_cats = self.cargar_categorias(rutaCat)

        try:
            id_cat, id_node = next(gen_cats)

            while True:
                grafo.get_node(id_node).add_cat(categorias[id_cat])
                id_cat, id_node = next(gen_cats)

        except StopIteration:
            pass

        return grafo