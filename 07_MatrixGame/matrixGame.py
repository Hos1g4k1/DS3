import numpy as np

def read_input():

    filePath = input("Unesite putanju do fajla")
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

    return n, m, matrix

def extractColumn(matrix, j):

    n = len(matrix)
    m = len(matrix[0])

    res = []

    for i in range(n):
        for k in range(m):

            if k == j:
                res.append(matrix[i][k])

    return res

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

matrix = np.array([[2, 1, 2, 3], [3, 1.5, 1, 2], [2, 2, 1, 1], [1, 1, 1, 1]])
#matrix = np.array([[1, -1, -1], [-1, -1, 3], [-1, -2, -1]])
matrix = reduce_dimension(matrix)
print(matrix)

