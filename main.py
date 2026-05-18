from src.Logic.WikiLoader import WikiLoader
from src.Spinner import Spinner
import os

from src.Logic import CSVWritters as csv, Algorithms as alg

def pagerank(grafo):
    """
    Llama a la función de PageRank para cada nodo.
    Solicita los valores de iteraciones y amortiguación.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    i = int(input("Iteraciones: "))
    d = float(input("Factor de amortiguación: "))

    print()

    spinner = Spinner("Cargando PageRank...")
    scores = alg.pagerank(grafo, i, d)
    spinner.stop()

    return sorted(scores.items(), key = lambda x: x[1], reverse = True)

def camino_corto(grafo):
    """
    Llama a la función del camino más corto entre dos nodos.
    Solicita los nombres de cada nodo, presenta todos aquellos con ese nombre y luego consulta por sus ids para la confimación.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    name1 = input("Introduce el nombre del nodo origen: ")
    name2 = input("Introduce el nombre del nodo destino: ")

    print(f"Nodos llamado {name1}: ")
    print(list(grafo.get_ids_by_name(name1)))
    print("-" * 20)
    print(f"Nodos llamado {name2}: ")
    print(list(grafo.get_ids_by_name(name2)))
    print()

    start = int(input("Id inicio: "))
    end = int(input("Id final: "))
    print()

    spinner = Spinner("Cargando camino...")
    path = grafo.bfs(start, end)
    spinner.stop()
    print()

    for i in path:
        nodo = grafo.get_node(i)
        print(f"-> {nodo.name} (id: {nodo.id})")

def ver_nodos(grafo):
    """
    Llama a la función del mostrar nodos.
    Solicita la cantidad de nodos para ver por consola.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    jump = int(input("Introduce los nodos por pag: "))

    gen = grafo.see_nodes(jump)

    try:
        while True:
            next(gen)
            key = input("\nIngrese cualquier letra para siguiente pagina (x para salir): ").lower()

            if (key == "x"):
                return

    except StopIteration:
        pass

def ver_cats(grafo):
    """
    Llama a la función del mostrar categorías.
    Solicita la cantidad de categorías para ver por consola.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    jump = int(input("Introduce las categorias por pag: "))

    gen = grafo.see_cats(jump)

    try:
        while True:
            next(gen)
            key = input("\nIngrese cualquier letra para siguiente pagina (x para salir): ").lower()

            if (key == "x"):
                return

    except StopIteration:
        pass

def menu(grafo):
    """
    Función principal, se encarga de solicitar por consola todas las opciones disponibles.
    Llama a todas las funciones correspondientes para una correcta ejecución del programa.

    Args:
        grafo (Graph): Grafo cargado con la información.
    """

    print("Taller 01: Prog. Científica")
    print("Por Martín Droguett, Lucas Munizaga y Francisco Romero.")
    print("Fecha: 15-05-2026")
    print("---------------------")

    option = 0

    pagerank_loaded = False

    scores = None

    print()

    while (option != 12):
        print("1. Cargar CSVs con informacion de grados de los nodos")
        print("2. Cargar CSV con PageRanks de cada nodo")
        print("3. Cargar CSV con informacion de categorias")
        print("4. Cargar CSV filtrando por categoria")
        print("5. Cargar CSV closeness (con sample k=100)")
        print("6. Obtener resumen del grafo")
        print("7. Obtener camino mas corto entre dos nodos")
        print("8. Hacer BFS desde un nodo origen")
        print("9. Hacer DFS desde un nodo origen")
        print("10. Ver nodos")
        print("11. Ver categorias")
        print("12. Salir")
        print("* Nota: Los archivos CSV se veran reflejados una vez termine el programa")
        option = int(input("> "))

        print()
        print("\033[H\033[J", end="")

        if option == 1:
            spinner = Spinner("Cargando CSV de grados...")

            csv.cargar_CSV_grados(grafo)

            spinner.stop()

        elif option == 2:

            if not pagerank_loaded:
                scores = pagerank(grafo)
                pagerank_loaded = True

            spinner = Spinner("Cargando CSV de PageRank...")
            csv.cargar_CSV_pagerank(grafo, scores)
            spinner.stop()

        elif option == 3:

            if not pagerank_loaded:
                scores = pagerank(grafo)
                pagerank_loaded = True

            spinner = Spinner("Cargando CSV de categorias...")
            csv.cargar_CSV_cat(grafo)
            spinner.stop()

        elif option == 4:
            id = int(input("Introduce el id de la categoria: "))

            spinner = Spinner("Cargando CSV de categoria filtrada...")
            csv.cargar_CSV_filtrado_cat(grafo, id)
            spinner.stop()

        elif option == 5:
            spinner = Spinner("Cargando Centralidades...")
            resultados = alg.calcular_closeness_centrality_rapido(grafo, k=100, spinner=spinner)

            spinner.change_text("Cargando CSV centralidad (4/4)...")
            csv.cargar_CSV_closeness_centrality(resultados)
            spinner.stop()

        elif option == 6:
            print("resumen final:", grafo.summary())

        elif option == 7:
            camino_corto(grafo)

        elif option == 8:
            id = int(input("Introduce el id del nodo origen: "))
            grafo.bfs(id, None, True)

        elif option == 9:
            id = int(input("Introduce el id del nodo origen: "))
            grafo.dfs(id, True)

        elif option == 10:
            ver_nodos(grafo)

        elif option == 11:
            ver_cats(grafo)

        elif option == 12:
            print("Saliendo...")

        else:
            print("--Opción inválida--")

        print()


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    spinner = Spinner("Cargando grafo...")

    fileLoader = WikiLoader()
    grafo = fileLoader.cargar_grafo()

    spinner.stop()

    menu(grafo)
