import numpy as np
import scipy.optimize
import scipy.optimize as opt

def read_input():

    filePath = input("Unesite putanju do fajla: ")
    file = open(filePath, "r")
    lines = file.readlines()

    n, m = lines[0].split(" ")
    n = int(n)
    m = int(m)
    matrix = np.zeros((n, m))

    for i in range(n):
        line = lines[i+1].split(" ")
        for j in range(m):
            matrix[i][j] = float(line[j])

    matrix = matrix.tolist()
    k = len(matrix[0])
    for i in range(n):
        if i < n-k:
            matrix[i].append(-1)
            matrix[i].append(1)
        else:
            k -= 1
            matrix[i].append(0)
            matrix[i].append(0)

    matrix[len(matrix)-1] = [0]*len(matrix[0])
    matrix[len(matrix)-2] = [0]*len(matrix[0])

    for i in range(m):
        matrix[len(matrix) - 1][i] = 1
        matrix[len(matrix) - 2][i] = -1

    return matrix

def extractColumn(matrix, j):

    n = len(matrix)
    m = len(matrix[0])

    res = []

    for i in range(n):
        for k in range(m):

            if k == j:
                res.append(matrix[i][k])

    return res


def solve_linear_programming_problem(c, A, b):
    res = scipy.optimize.linprog(c, A, b)
    f = np.round(res["fun"], 8)
    y = np.round(res["x"], 8)
    return f, y
'''
    Funkcija koja izdvaja red koji treba izbaciti
'''
def getDomRows(matrix):

    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            row1 = matrix[i]
            row2 = matrix[j]

            if compareVectors(row1, row2):
                return j

    return None

def compareVectors(vec1, vec2):

    res = True

    for i in range(len(vec1)):
        if vec1[i] < vec2[i]:
            return False

    return True
'''
    Funkcija koja izdvaja kolonu koju treba izbaciti
'''
def getDomCols(matrix):

    m = len(matrix[0])

    for i in range(m):

        for j in range(m):

            if i == j:
                continue

            col1 = extractColumn(matrix, i)
            col2 = extractColumn(matrix, j)

            if compareVectors(col1, col2):
                return i

    return None
'''
    Izbacuje red iz matrice i vraca novonastalu matricu
'''
def updateMatrixRows(matrix, row):

    n = len(matrix)
    m = len(matrix[0])

    new_matrix = np.zeros((n-1, m))

    row_cout = 0
    for i in range(n):
        if i == row:
            continue
        for j in range(m):
            new_matrix[row_cout][j] = matrix[i][j]

        row_cout += 1

    return new_matrix

'''
    Izbacuje kolonu iz matrice i vraca novonastalu matricu
'''
def updateMatrixCols(matrix, col):

    n = len(matrix)
    m = len(matrix[0])

    new_matrix = np.zeros((n, m-1))

    for i in range(n):
        col_cout = 0
        for j in range(m):
            if j == col:
                continue
            new_matrix[i][col_cout] = matrix[i][j]

            col_cout += 1

    return new_matrix

'''
    Vrsi postupak dominacije i vraca matricu
    minimalnih mogucih dimenzija
'''
def reduce_dimension(matrix):

    change = True

    while change:

        x = getDomRows(matrix)

        if x is not None:
            matrix = updateMatrixRows(matrix, x)
            print(matrix)
            continue

        y = getDomCols(matrix)

        if y is not None:
            matrix = updateMatrixCols(matrix, y)
            print(matrix)
            continue

        break

    return matrix

A = read_input()
c_min = list()
n = len(A)
m = len(A[0])
# Formiramo ciljnu funkciju
for i in range(m):
    if i == m-1:
        c_min.append(-1)
    elif i == m-2:
        c_min.append(1)
    else:
        c_min.append(0)

# Formiramo vektor desne strane
b_min = list()
for i in range(n):
    if i == n-2:
        b_min.append(-1)
    elif i == n-1:
        b_min.append(1)
    else:
        b_min.append(0)

f, y = solve_linear_programming_problem(c_min, A, b_min)

print(f"Vrednost igre je {f}")
print(f"Optimalna tacka je y = {y[:-2]}")
