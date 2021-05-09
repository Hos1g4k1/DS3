
class Graph:

    def __init__(self, v):
        self.v = v                                                          # Broj cvorova
        self.visited = [False for _ in range(v)]                            # Vektor u kom se pamti da li je cvor posecen
        self.adjacency_list = [[] for _ in range(v)]                        # Lista povezanosti
        self.degrees = [0 for _ in range(v)]                                # Vektor u kom se pamte stepeni cvorova

    # Funkcija koja dodaje granu u graf
    # Kako je graf neusmeren, dodaju se grane u
    # u oba pravca
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

            # Stack may contain same vertex twice. So
            # we need to print the popped item only
            # if it is not visited.
            if (not self.visited[s]):
                print(s, end=' ')
                self.visited[s] = True

            # Get all adjacent vertices of the popped vertex s
            # If a adjacent has not been visited, then push it
            # to the stack.
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

        # Ukoliko je to jedina grana iz tog cvora
        # sigurno je most
        if len(self.adjacency_list[u]) == 1:
            return True

        if len(self.adjacency_list[u]) != 1 and v == end:
            return False

        return True

    def print_euler_path_or_cycle(self, u, end):

        for v in self.adjacency_list[u]:

            if self.is_valid_edge(u, end, v):
                print(f"{u} -> {v}")
                self.remove_edge(u, v)
                self.print_euler_path_or_cycle(v, end)
                break

    def fleury(self):

        # Provera da li u grafu postoji Ojlervov ciklus
        count_odd = self.num_of_odd_vertices()
        if count_odd == 0:
            start, end = self.find_node_with_even_degree()
            self.print_euler_path_or_cycle(start, end)
        # Provera da li u grafu postoji Ojlerov put
        elif count_odd == 2:
            start, end = self.find_node_with_odd_degree()
            self.print_euler_path_or_cycle(start, end)

def main():

    # Primer za Ojlerov ciklus
    # g = Graph(5)
    #
    # g.add_edge(0, 1)
    # g.add_edge(0, 2)
    # g.add_edge(0, 3)
    # g.add_edge(1, 2)
    # g.add_edge(1, 3)
    # g.add_edge(2, 3)
    # g.add_edge(2, 4)
    # g.add_edge(3, 4)
    #
    # g.fleury()

    g = Graph(5)  # Total 5 vertices in graph
    g.add_edge(1, 0)
    g.add_edge(0, 2)
    g.add_edge(2, 1)
    g.add_edge(0, 3)
    g.add_edge(1, 4)

    # g.DFS(0)
    g.BFS(0)

main()
