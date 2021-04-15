import numpy as np
import scipy.optimize

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

def form_c_vector(n, m):

    c_min = list()

    for i in range(m):
        if i == m-1:
            c_min.append(-1)
        elif i == m-2:
            c_min.append(1)
        else:
            c_min.append(0)

    return c_min

def form_b_vector(n, m):
    b_min = list()
    for i in range(n):
        if i == n - 2:
            b_min.append(-1)
        elif i == n - 1:
            b_min.append(1)
        else:
            b_min.append(0)

    return b_min

def add_v1_v2(matrix):

    n = len(matrix)

    for i in range(n):
        matrix[i].append(-1)
        matrix[i].append(1)

    return matrix

def add_positive_constraints(matrix):

    n = len(matrix)
    m = len(matrix[0])

    for i in range(m-2):
        vec = [0]*(m)
        vec[i] = -1
        matrix.append(vec)

    return matrix

def add_sum_1_constraints(matrix):
    m = len(matrix[0])

    vec1 = [-1]*m
    vec1[-1] = 0
    vec1[-2] = 0
    matrix.append(vec1)

    vec2 = [1]*m
    vec2[-1] = 0
    vec2[-2] = 0
    matrix.append(vec2)

    return matrix


A = read_input()
A = A.tolist()
B = np.array(A).tolist()

A = add_v1_v2(A)

print(B)

# A = add_positive_constraints(A)
A = add_sum_1_constraints(A)

print(B)

n = len(A)
m = len(A[0])
# Formiramo ciljnu funkciju
c_min = form_c_vector(n, m)
# Formiramo vektor desne strane
b_min = form_b_vector(n, m)

# print(f"b = {b_min}")
# print(f"c = {c_min}")
# print("A")
# for x in A:
    # print(x)

f_min, y = solve_linear_programming_problem(c_min, A, b_min)

print(f"Vrednost igre je {f_min}")
print(f"Optimalna tacka je y = {y[:-2]}")

B = (np.array(B).T).tolist()
B = add_v1_v2(B)
B = add_sum_1_constraints(B)
for i in range(len(B)):
    for j in range(len(B[0])):
        B[i][j] = -1*B[i][j]

b_max = form_b_vector(len(B), len(B[0]))
c_max = form_c_vector(len(B), len(B[0]))
for i in range(len(b_max)):
    b_max[i] = -b_max[i]

for i in range(len(c_max)):
    c_max[i] = -c_max[i]

# print(f"b = {b_max}")
# print(f"c = {c_max}")

f_max, x = solve_linear_programming_problem(c_max, B, b_max)

print(f"Optimalna tacka je y = {x[:-2]}")
