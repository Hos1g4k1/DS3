def readInput():

    filePath = input("Unesite putanju do fajla: ")
    file = open(filePath)

    lines = file.readlines()

    file.close()

    line = lines[0].split(" ")
    v = int(line[0])
    source = int(line[1])
    sink = int(line[2])

    matrix = [[0 for _ in range(v)] for _ in range(v)]
    i = 0
    for l in range(1, len(lines)):
        line = lines[l]
        line = line.split(" ")
        for j in range(v):
            matrix[i][j] = int(line[j])
        i = i+1

    return matrix, source, sink


class Graph:

    def __init__(self, graph):
        self.graph = graph
        self.v = len(graph)

    def BFS(self, s, t, parent):

        visited = [False] * (self.v)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.v)
        max_flow = 0

        while self.BFS(source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

graph, source, sink = readInput()

g = Graph(graph)

print(f"Max Flow: {g.ford_fulkerson(source, sink)}")
