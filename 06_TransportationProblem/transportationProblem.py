import numpy as np
import math


def readInput():

    filePath = input("Unesite putanju do fajla: ")
    file = open(filePath, "r")
    lines = file.readlines()

    # Ucitavanje dimenzija matrice cena
    broj_redova, broj_kolona = lines[0].split(" ")
    broj_redova = int(broj_redova)
    broj_kolona = int(broj_kolona)

    # Ucitavanje matrice cena
    matrix = np.zeros((broj_redova, broj_kolona))
    for i in range(broj_redova):
        row = lines[i+1].split(" ")
        for j in range(broj_kolona):
            matrix[i][j] = float(row[j])

    a = list()  # Vektor a_i
    b = list()  # Vektor b_j

    row = lines[len(lines)-2].split(" ")
    for x in row:
        a.append(float(x))

    row = lines[len(lines) - 1].split(" ")
    for x in row:
        b.append(float(x))

    return broj_redova, broj_kolona, matrix, a, b


def make_graph(n):

    res = []
    for i in range(n):
        res.append([])

    return res


def add_edge(graph, x, y):
    graph[x].append(y)
    return graph


def cords_to_index(i, j, m):
    return i * m + j


def index_to_cords(index, m):
    return index / m, index % m


def is_stable_path(path, n, m):

    last_state = None
    current_state = None

    for i in range(1, len(path)):
        x1, y1 = index_to_cords(path[i-1], m)
        x2, y2 = index_to_cords(path[i], m)

        if x1 == x2:
            current_state = 'row'
        elif y1 == y2:
            current_state = 'col'
        else:
            return False

        if current_state == last_state:
            return False

        last_state = current_state

    x1, y1 = index_to_cords(path[len(path)-1], m)
    x2, y2 = index_to_cords(path[0], m)

    if x1 == x2:
        current_state = 'row'
    elif y1 == y2:
        current_state = 'col'
    else:
        return False

    if current_state == last_state:
        return False

    return True


def find_cycle(graph, start_node, t_n, t_m):

    size = len(graph)

    parents = [-1]*size
    on_stack = [False]*size

    s = list()
    s.append((start_node, 0))
    on_stack[start_node] = True

    path = []

    while len(s) > 0:

        node = s[len(s)-1][0]
        index = s[len(s)-1][1]

        if index == len(graph[node]):
            s.pop(len(s)-1)
            on_stack[node] = False
            parents[node] = -1
            continue

        s[len(s)-1][1] += 1

        child = graph[node][index]

        if child == start_node and parents[node] != start_node:

            if len(s) % 2 == 0:

                path.append(start_node)
                n = node

                while n != -1:

                    path.append(n)
                    n = parents[n]

                if is_stable_path(path, t_n, t_m):
                    return path
                else:
                    path = []

        if not on_stack[child]:
            s.append((child, 0))
            parents[child] = node
            on_stack[child] = True

    return []


def form_graph(theta_i, theta_j, matrix, new_matrix):

    n = len(new_matrix)
    m = len(new_matrix[0])

    theta = float('inf')

    graph = make_graph(n*m)

    for i in range(n):

        for j in range(m):

            if math.isnan(new_matrix[i][j]) and (i != theta_i or j != theta_j):
                continue

            for k in range(n):

                if i == k:
                    continue

                if math.isnan(new_matrix[k][i]) and (k != theta_i or j != theta_j):
                    continue

                graph = add_edge(graph, cords_to_index(i, j, m), cords_to_index(k, j, m))

            for k in range(m):

                if j == k:
                    continue

                if math.isnan(new_matrix[i][k]) and (i != theta_i or k != theta_j):
                    continue

                graph = add_edge(graph, cords_to_index(i, j, m), cords_to_index(i, k, m))

    cycle = find_cycle(graph, cords_to_index(theta_i, theta_j, m), n, m)

    for k in range(len(cycle)):
        if k % 2 == 0:
            continue

        i, j = index_to_cords(cycle[k], m)
        theta = min(theta, matrix[i][j])


def find_min(matrix, discarded_rows, discarded_cols):

    res = float('inf')
    res_i = None
    res_j = None

    for i in range(len(matrix)):
        if i in discarded_rows:
            continue
        for j in range(len(matrix[0])):
            if j in discarded_cols:
                continue
            if matrix[i][j] < res:
                res = matrix[i][j]
                res_i = i
                res_j = j

    return res_i, res_j, res


def calculate_potentials(matrix, new_matrix):

    print(matrix)
    print(new_matrix)

    potential_a = [0.0] * len(matrix)
    potential_b = [0.0] * len(matrix[0])

    calculated_rows = set()
    calculated_cols = set()

    basis_in_row = [0] * len(matrix)
    basis_in_col = [0] * len(matrix[0])

    for i in range(len(new_matrix)):
        for j in range(len(matrix[0])):
            if not math.isnan(new_matrix[i][j]):
                basis_in_row[i] += 1
                basis_in_col[j] += 1

    # print(f"basis in row = {basis_in_row}")
    # print(f"basis in col = {basis_in_col}")

    # Ukoliko je ova promenljiva True, znaci da posmatramo red ciji indeks
    # se nalazi u promenljivoj index, ukoliko je False posmatramo kolonu
    row_col = True

    max_count = -1
    index = None

    for i in range(len(matrix)):
        if basis_in_row[i] > max_count:
            max_count = basis_in_row[i]
            row_col = True
            index = i

    for i in range(len(matrix[0])):
        if basis_in_col[i] > max_count:
            max_count = basis_in_col[i]
            row_col = False
            index = i

    if row_col:
        potential_a[index] = 0.0
        calculated_rows.add(index)
    else:
        potential_b[index] = 0.0
        calculated_cols.add(index)

    s = list()
    s.append((index, row_col))

    while len(s) > 0:

        index = s[len(s)-1][0]
        is_row = s[len(s)-1][1]
        s.pop()

        if is_row:
            for j in range(len(matrix[0])):
                if math.isnan(new_matrix[index][j]):
                    continue

                if j not in calculated_cols:
                    potential_b[j] = matrix[index][j] - potential_a[index]
                    calculated_cols.add(j)
                    s.append((j, False))
        else:
            for i in range(len(matrix)):

                if math.isnan(new_matrix[i][index]):
                    continue

                if i not in calculated_rows:
                    potential_a[i] = matrix[i][index] - potential_b[index]
                    calculated_rows.add(i)
                    s.append((i, True))

    return potential_a, potential_b

def find_start_tetha(new_matrix, matrix, potential_a, potential_b):

    theta_i = None
    theta_j = None
    theta = float('inf')

    n = len(potential_a)
    m = len(potential_b)

    for i in range(n):
        for j in range(m):
            if not math.isnan(new_matrix[i][j]):
                continue

            p = matrix[i][j] - potential_a[i] - potential_b[j]

            if p < 0:
                if p < theta:
                    theta = p
                    theta_i = i
                    theta_j = j

    return theta_i, theta_j

def closed_transportation_problem(matrix, a, b):

    # Formiranje pocetnog resenja metodom najnizih cena

    br_redova = len(matrix)
    br_kolona = len(matrix[0])

    # Trebace za kasnije
    a_copy = a.copy()
    b_copy = b.copy()

    new_matrix = np.zeros((br_redova, br_kolona))

    for i in range(br_redova):
        for j in range(br_kolona):
            new_matrix[i][j] = None

    discarded_cols = []
    discarded_rows = []

    pos_i = None
    pos_j = None

    max_iteration = br_kolona + br_redova - 1
    iter = 0

    while(iter < max_iteration):
        pos_i, pos_j, minimum = find_min(matrix, discarded_rows, discarded_cols)
        # print(f"Iter = {iter}")
        # print(f"Vektor a: {a}")
        # print(f"Vektor b: {b}")
        # print()
        # print()
        #
        # print(f"Minumum: {minimum}")
        # print(f"Pos_i = {pos_i}")
        # print(f"Pos_j = {pos_j}")

        if a[pos_i] < b[pos_j]:
            new_matrix[pos_i][pos_j] = a[pos_i] # Dodajemo kapicu
            x = a[pos_i]
            a[pos_i] -= x                       # Azuriramo a_i
            b[pos_j] -= x                       # Azuriramo b_j
            discarded_rows.append(pos_i)        # Azuriramo nedostupne redove
        else:
            new_matrix[pos_i][pos_j] = b[pos_j]
            x = b[pos_j]
            a[pos_i] -= x
            b[pos_j] -= x
            discarded_cols.append(pos_j)

        # print()
        # print(new_matrix)

        iter += 1

    a = a_copy
    b = b_copy

    #print(new_matrix)
    # Optimizacija resenja metodom potencijala

    potential_a, potential_b = calculate_potentials(matrix, new_matrix)

    print(f"Potencijali za a: {potential_a}")
    print(f"Potencijali za b: {potential_b}")



# closed_transportation_problem([[20, 11, 15, 13], [17, 14, 12, 13], [15, 12, 18, 18]], [2, 6, 7], [3, 3, 4, 5])

def transportation_problem():

    #broj_redova, broj_kolona, matrix, a, b = readInput()

    broj_redova = 3
    broj_kolona = 4
    matrix = [[20, 11, 15, 13], [17, 14, 12, 13], [15, 12, 18, 18]]
    a = [2, 6, 7]
    b = [3, 3, 4, 5]

    sum_a = sum(a)
    sum_b = sum(b)

    if sum_a == sum_b:
        print("Problem je zatvorenog tipa!")
        closed_transportation_problem(matrix, a, b)
    else:
        print("Problem je otvorenog tipa!")
        print("Prebacujemo ga na problem zatvorenog tipa!")
        # Treba dodati vestacku kolonu
        if sum_a > sum_b:
            new_matrix = np.zeros((broj_redova, broj_kolona + 1))

            for i in range(broj_redova):
                for j in range(broj_kolona + 1):
                    if j != broj_kolona:
                        new_matrix[i][j] = matrix[i][j]
                    else:
                        new_matrix[i][j] = 1000

            b.append(sum_a - sum_b)

            print(new_matrix)
            print(a)
            print(b)

            closed_transportation_problem(matrix, a, b)
            #res = closed_transportation_problem(matrix, a, b)
            #print(f"Rezultat = {res}")
        # Treba dodati vestacku vrstu
        else:
            new_matrix = np.zeros((broj_redova + 1, broj_kolona))
            for i in range(broj_redova + 1):
                for j in range(broj_kolona):
                    if i != broj_redova:
                        new_matrix[i][j] = matrix[i][j]
                    else:
                        new_matrix[i][j] = 1000

            a.append(sum_b - sum_a)

            print(new_matrix)
            print(a)
            print(b)

            closed_transportation_problem(matrix, a, b)
            # res = closed_transportation_problem(new_matrix, a, b)
            # print(f"Rezultat = {res}")


transportation_problem()
