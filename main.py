from Domain.Graph import Graph
archEdges = open("Data/top-20-links.txt", "r", encoding="utf-8")
archNames = open("Data/top-20-articles.txt", "r", encoding="utf-8")

graph = Graph()

prev = -1
lineEdges = archEdges.readline().strip()

while lineEdges != "":
    partsEdges = lineEdges.split(" ")

    origin = int(partsEdges[0])
    dest = int(partsEdges[1])

    graph.connect(graph.get_node(origin), graph.get_node(dest))

    if prev != origin:
        lineNames = archNames.readline().strip()
        graph.setName(graph.get_node(origin), lineNames.replace(f"{origin} ", "").strip())

    prev = origin

    lineEdges = archEdges.readline().strip()

graph.debug()

print("===================================")

graph.bfs(1)

print("====================================")

graph.dfs(1)

archEdges.close()
archNames.close()
