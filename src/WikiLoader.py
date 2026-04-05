from pathlib import Path
import Node
import Graph
class WikiLoader:
    def __init__(self):
        self.dir_dataset=Path().resolve().parent / "dataset"
    
    def __cargar_nombres_categorías(self):
        ruta = self.dir_dataset / "wiki-topcats-categories.txt"
        categorias = {}

        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:

                if not linea or ";" not in linea:
                    continue

                parte_categoria,ids = linea.split(";")
                nombre_categoria = parte_categoria.replace("Category:","").strip()
                ids = ids.split(" ").strip()

                for id in ids:
                    categorias[id] = nombre_categoria
        return categorias

    def __cargar_nombres_articulos(self):
        ruta = self.dir_dataset / "wiki-topcats-page-names.txt"
        nombres = {}

        with open(ruta,"r",encoding="utf-8") as file:
            for linea in file:
                if not linea:
                    continue
                id,nombre_articulo = linea.split(" ",1)
                nombres[id]=nombre_articulo
        return nombres
    
    def __cargar_enlaces_articulos(self):
        ruta = self.dir_dataset / "wiki-topcats"
        edges = {}

        with open(ruta,"r",encoding="utf-8") as file:
            index = ""
            for linea in file:
                if not linea:
                    continue
                id1,id2 = linea.strip().split(" ")
                if  id1!=index:
                    index = id1
                    edges[index] = [id2]
                else:
                    edges[index].append(id2)
        return edges

    def cargar_grafo(self):
        categorias = self.__cargar_nombres_categorías()
        nombres = self.__cargar_nombres_articulos()
        edges = self.__cargar_enlaces_articulos()
        grafo = Graph()

        for id,name in nombres:
            grafo.add(id,name,edges[id],categorias[id])

        return grafo