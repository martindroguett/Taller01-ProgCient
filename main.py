from Domain.Node import Node
archEdges = open("Data/top-20-links.txt", "r", encoding="utf-8")
archNames = open("Data/top-20-articles.txt", "r", encoding="utf-8")

nodes = { }

prev = -1

while prev < 20:

    lineEdges = archEdges.readline().strip()
    partsEdges = lineEdges.split(" ")

    origin = int(partsEdges[0])
    dest = int(partsEdges[1])

    myNodeOrigin = nodes.get(origin, Node(origin))
    nodes[origin] = myNodeOrigin

    myNodeDest = nodes.get(dest, Node(dest))
    nodes[dest] = myNodeDest
    myNodeOrigin.connect(dest, myNodeDest)

    if (prev != origin):
        lineNames = archNames.readline().strip()

        myNodeOrigin.setName(lineNames.replace(f"{origin} ", "").strip())

    prev = origin

for node in nodes.values():
    print("--------------")
    print(node.id,node.name)
    print(f"LENGHT OF LINKS: {len(node.links)}")
    for n in node.links:
        if n == None:
            print(f"PASS AUF: {n}")
        print(n)

archEdges.close()
archNames.close()