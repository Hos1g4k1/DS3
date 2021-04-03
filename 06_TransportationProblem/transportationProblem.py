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

def closed_transportation_problem(matrix, a, b):
    pass

    # Formiranje pocetnog resenja metodom najnizih cena

    # Optimizacija resenja metodom potencijala

def transportation_problem():

    broj_redova, broj_kolona, matrix, a, b = readInput()

    sum_a = sum(a)
    sum_b = sum(b)

    if sum_a == sum_b:
        closed_transportation_problem(matrix, a, b)
    else:
        # Treba dodati vestacku vrstu
        if sum_a > sum_b:
            new_matrix = np.zeros((broj_redova+1, broj_kolona))
            for i in range(broj_redova+1):
                for j in range(broj_kolona):
                    if i != broj_redova:
                        new_matrix[i][j] = matrix[i][j]
                    else:
                        new_matrix[i][j] = 50

            b.append(sum_a - sum_b)
            res = closed_transportation_problem(new_matrix, a, b)
            print(f"Rezultat = {res}")
        # Treba dodati vestacku kolonu
        else:
            new_matrix = np.zeros((broj_redova, broj_kolona+1))

            for i in range(broj_redova+1):
                for j in range(broj_kolona):
                    if j != broj_kolona:
                        new_matrix[i][j] = matrix[i][j]
                    else:
                        new_matrix[i][j] = 50

            a.append(sum_b-sum_a)
            res = closed_transportation_problem(matrix, a, b)
            print(f"Rezultat = {res}")
