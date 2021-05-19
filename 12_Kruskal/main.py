from GraphComponents.components import GraphComponents

def readInput():

    path = input("Unesite putanju do fajla: ")
    file = open(path, "r")

    lines = file.readlines()

    V = int(lines[0])
    edges = []

    for i in range(1, len(lines)):
        line = lines[i].split(" ")
        u = int(line[0])
        v = int(line[1])
        w = int(line[2])

        edges.append([u, v, w])

    file.close()

    return V, edges

class Graph:
    def __init__(self, V):
        self.adjacency_list = []
        self.V = V
        self.total = 0

    # Funkcija koja dodaje tezinsku granu u graf
    def add_edge(self, u, v, weight):
        self.adjacency_list.append([u, v, weight])

    # Funkcija koja pronalazi koren nekog cvora
    # Koristi se pri odredjivanju kojoj komponenti
    # povezanosti taj cvor pripada
    def findRoot(self, parent, i):
        if parent[i] == i:
            return i
        return self.findRoot(parent, parent[i])

    # Funkcija koja vrsi uniju cvorova neke
    # dve komponente povezanosti
    def union(self, parent, rank, x, y):
        xroot = self.findRoot(parent, x)
        yroot = self.findRoot(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    # Funkcija koja predstavlja Kraskalov algoritam za
    # trazenje minimalne razapinjuce sume
    def Kruskal(self, numOfEdges):
        result = []
        i = 0

        # Sortiramo grane u neopadajuci poredak po tezini grane
        self.adjacency_list = sorted(self.adjacency_list, key=lambda item: item[2])

        parent = []
        rank = []

        # Svaki cvor je na pocetku samostalna
        # komponenta povezanosti
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Broj uzetih grana jeste suma grana
        # minimalnih razapinjucih stabala
        # za svaku komponentu povezanosti
        while len(result) < numOfEdges:
            # Uzimamo granu najmanje tezine
            u, v, w = self.adjacency_list[i]
            i = i + 1
            # Odredjujemo korene za oba kraja te grane
            x = self.findRoot(parent, u)
            y = self.findRoot(parent, v)

            # Ukoliko su razliciti, cvorovi ne pripadaju istoj komponenti
            # povezanosti i onda treba tu granu ukljuciti u resenje
            if x != y:
                self.union(parent, rank, x, y)
                self.total = self.total + w
                result.append([u, v, w])

        return result

def main():
    v, edges = readInput()

    gc = GraphComponents(v)
    for i in range(len(edges)):
        gc.addEdge(edges[i][0], edges[i][1])

    cc = gc.connectedComponents()

    numOfEdges = 0
    for c in cc:
        numOfEdges += len(c)-1

    g = Graph(v)
    for i in range(len(edges)):
        g.add_edge(edges[i][0], edges[i][1], edges[i][2])
    result = g.Kruskal(numOfEdges)

    print("Minimalna razapinjuca suma: ")
    for p, c, weight in result:
        print(str(p) + " - " + str(c))
    print("Tezina: ", g.total)


if __name__ == '__main__':
    main()