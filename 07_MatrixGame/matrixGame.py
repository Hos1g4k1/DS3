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


def FMM(c, A, b):
    res = scipy.optimize.linprog(c, A, b)
    return res["fun"], res["x"]


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

# matrix = np.array([[2, 1, 2, 3], [3, 1.5, 1, 2], [2, 2, 1, 1], [1, 1, 1, 1]])
# #matrix = np.array([[1, -1, -1], [-1, -1, 3], [-1, -2, -1]])
# matrix = reduce_dimension(matrix)
# print(matrix)

# A = [[2, 1, 2, 3, -1],
#      [3, 1.5, 1, 2, -1],
#      [2, 2, 1, 1, -1],
#      [1, 1, 1, 1, -1],
#      [1, 1, 1, 1, 0],
#      [-1, -1, -1, -1, 0]]
#
# b = [0, 0, 0, 0, 1, -1]
# c = [0, 0, 0, 0, 1]

# num = len(A[0])-1

#
# A = [[1, -1, -1, 1, -1, 1],
#      [-1, -1, 3, 1, -1, 1],
#      [-1, -2, -1, 1, -1, 1],
#      [1, 1, 1, 1, 0, 0]]
#
# num = len(A[0])-3
#
# c = [0, 0, 0, 0, 1, -1]
# b = [0, 0, 0, 1]

A = read_input()

c_min = list()
n = len(A)
m = len(A[0])
for i in range(m):
    if i == m-1:
        c_min.append(-1)
    elif i == m-2:
        c_min.append(1)
    else:
        c_min.append(0)

b_min = list()

for i in range(n):
    if i == n-2:
        b_min.append(-1)
    elif i == n-1:
        b_min.append(1)
    else:
        b_min.append(0)

# print("--------------------------------------")
# for i in range(n):
#     print(A[i])
# print("--------------------------------------")
# print(b_min)
# print("--------------------------------------")
# print(c_min)

f, y = FMM(c_min, A, b_min)
f = np.round(f, 8)
y = np.round(y, 8)

print(f"Vrednost igre je {f}")
print(f"Optimalna tacka je y = {y[:-2]}")
