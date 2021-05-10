
class Graph:

    def __init__(self, v):
        self.v = v                                            # Broj cvorova
        self.visited = [False for _ in range(v)]              # Vektor u kom se pamti da li je cvor posecen
        self.adjacency_list = [[] for _ in range(v)]          # Lista povezanosti
        self.degrees = [0 for _ in range(v)]                  # Vektor u kom se pamte stepeni cvorova

    # Funkcija koja dodaje granu u graf
    # Kako je graf neusmeren, dodaju se grane u
    # u oba smera
    def add_edge(self, u, v):
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

        # Azuriramo stepene cvorova
        self.degrees[u] += 1
        self.degrees[v] += 1

    def DFS(self, s):
        # Na pocetku su svi cvorovi neposeceni
        self.visited = [False for i in range(self.v)]

        stack = []

        # Ubacujemo pocetni cvor u stek
        stack.append(s)

        # Sve dok imamo elemenata na steku
        while (len(stack)):
            # Uzimamo onaj sa vrha
            s = stack[-1]
            stack.pop()

            # Ubacujemo samo one cvorove
            # koje vec nismo posetili
            if (not self.visited[s]):
                print(s, end=' ')
                self.visited[s] = True

            # Prolazimo kroz sve susede cvora s
            # i dodajemo u stek one koji nisu
            # poseceni
            for node in self.adjacency_list[s]:
                if not self.visited[node]:
                    stack.append(node)

    def BFS(self, s):

        # Na pocetku su svi cvorovi neposeceni
        self.visited = [False for i in range(self.v)]

        queue = []

        # Obelezavamo pocetni cvor kao posecen
        # i dodajemo ga u red
        queue.append(s)
        self.visited[s] = True

        # Sve dok red nije prazan
        while queue:

            # Uzimamo cvor sa vrha reda
            s = queue.pop(0)
            print(s, end=" ")

            # Dodajemo svakog neposecenog suseda
            # trenutnog cvora u red
            for node in self.adjacency_list[s]:
                if self.visited[node] == False:
                    queue.append(node)
                    self.visited[node] = True

    # Funkcija koja pronalazi broj cvorova neparnog stepena
    def num_of_odd_vertices(self):

        count_odd = 0

        for i in range(self.v):
            if self.degrees[i] % 2:
                count_odd += 1

        return count_odd

    # Funkcija koja pronalazi cvorove neparnog stepena
    def find_node_with_odd_degree(self):

        first = -1
        second = -1

        for i in range(self.v):
            if self.degrees[i] % 2 == 1 and first == -1:
                first = i
            elif self.degrees[i] % 2 == 1:
                second = i

        return first, second

    # Funkcija koja pronalazi cvorove parnog stepena
    def find_node_with_even_degree(self):

        first = -1
        second = -1

        for i in range(self.v):
            if self.degrees[i] % 2 == 0 and self.degrees[i] > 0 and first == -1:
                first = i
            elif self.degrees[i] % 2 == 0 and self.degrees[i] > 0:
                second = i

        return first, second

    # Funkcija koja izbacuje granu iz grafa
    def remove_edge(self, u, v):

        self.adjacency_list[u].remove(v)
        self.adjacency_list[v].remove(u)

        # Azuriramo stepene cvorova
        self.degrees[u] -= 1
        self.degrees[v] -= 1

    # Proveravamo da li je grana most
    def is_valid_edge(self, u, end, v):

        # Ukoliko je preostala samo jedna grana
        # ona je most i treba je ukloniti
        if len(self.adjacency_list[u]) == 1:
            return True

        # Ukoliko imamo vise grana i ova je bas most
        # ne uklanjamo nju
        if len(self.adjacency_list[u]) != 1 and v == end:
            return False

        return True
    # Funkcija koja implementira Flerijev algoritam
    def print_euler_path_or_cycle(self, u, end):

        # Prolazimo kroz listu suseda cvora u
        for v in self.adjacency_list[u]:
            # Ukoliko grana od u do v treba da se ubaci
            if self.is_valid_edge(u, end, v):
                # Ispisujemo je
                print(f"{u} -> {v}")
                # Izbacujemo je iz grafa
                self.remove_edge(u, v)
                # I rekurzivno nastavljamo dalje
                self.print_euler_path_or_cycle(v, end)
                break

    def fleury(self):

        # Provera da li u grafu postoji Ojlervov ciklus
        count_odd = self.num_of_odd_vertices()
        if count_odd == 0:
            print("Graf ima Ojlerov ciklus!")
            start, end = self.find_node_with_even_degree()
            self.print_euler_path_or_cycle(start, end)
        # Provera da li u grafu postoji Ojlerov put
        elif count_odd == 2:
            print("Graf ima Ojlerov put!")
            start, end = self.find_node_with_odd_degree()
            self.print_euler_path_or_cycle(start, end)
        else:
            print("Graf nema ni Ojlerov ciklus ni Ojlerov put")

# Funckija koja pravi graf na osnovu podataka
# u nekom fajlu
def make_graph():

    path = input("Unesite putanju do fajla: ")
    file = open(path, "r")

    lines = file.readlines()
    v = int(lines[0])
    # Pravimo graf sa v cvorova
    g = Graph(v)

    for i in range(1, len(lines)):
        u, v = lines[i].split(" ")
        u = int(u)
        v = int(v)
        # Dodajemo granu neusmerenog grafa u v
        g.add_edge(u, v)

    file.close()
    return g

def main():
    g = make_graph()
    g.DFS(0)
    print()
    g.BFS(0)
    print()
    g.fleury()

main()
