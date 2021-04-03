import numpy as np

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

    a = [] # Vektor a_i
    b = [] # Vektor b_j

    row = lines[len(lines)-2].split(" ")
    for x in row:
        a.append(float(x))

    row = lines[len(lines) - 1].split(" ")
    for x in row:
        b.append(float(x))

    return broj_redova, broj_kolona, matrix, a, b

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

def closed_transportation_problem(matrix, a, b):
    #pass

    # Formiranje pocetnog resenja metodom najnizih cena

    br_redova = len(matrix)
    br_kolona = len(matrix[0])

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

    #print(new_matrix)
    # Optimizacija resenja metodom potencijala

# closed_transportation_problem([[20, 11, 15, 13], [17, 14, 12, 13], [15, 12, 18, 18]], [2, 6, 7], [3, 3, 4, 5])

def transportation_problem():

    broj_redova, broj_kolona, matrix, a, b = readInput()

    sum_a = sum(a)
    sum_b = sum(b)

    if sum_a == sum_b:
        closed_transportation_problem(matrix, a, b)
    else:
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
            res = closed_transportation_problem(matrix, a, b)
            print(f"Rezultat = {res}")
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
            res = closed_transportation_problem(new_matrix, a, b)
            print(f"Rezultat = {res}")

