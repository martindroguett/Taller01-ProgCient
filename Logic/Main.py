from Domain.Node import Node

archEdges = open("../Data/wiki-topcats.txt", "r", encoding="utf-8")
archNames = open("../Data/wiki-topcats-page-names.txt", "r", encoding="utf-8")

nodes = { }

prev = -1

while prev < 20:

    lineEdges = archEdges.readline()
    partsEdges = lineEdges.split(" ")

    origin = int(partsEdges[0])
    dest = int(partsEdges[1])

    myNodeOrigin = nodes.get(origin, Node(origin))
    nodes[origin] = myNodeOrigin

    myNodeDest = nodes.get(dest, Node(dest))
    nodes[dest] = myNodeDest
    myNodeOrigin.connect(dest, myNodeDest)

    if (prev != origin):
        lineNames = archNames.readline()

        myNodeOrigin.setName(lineNames.replace(f"{origin} ", "").strip())

    prev = origin

for node in nodes.values():
    print(node.id, node, node.name, node.links)

archEdges.close()
archNames.close()