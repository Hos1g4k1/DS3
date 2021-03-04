def printMatrix(A):
    for row in A:
        str = ""
        for elem in row:
            str += elem.__str__() + " "
        print(str)

def printVector(b):
    str = ""
    for elem in b:
        str += elem.__str__() + " "
    print(str)

'''
    Ova funkcija se poziva kada su uklonjenje sve promenljive sem poslednje
    Vrsi se presek svih nejednakosti i vraca se interval
'''
def find_intersection(A, b):

    m = len(b)
    left_bound = float('-inf')
    right_bound = float('inf')

    for p in range(0, m):
        if A[p][0] == 0:
            if b[p] > 0:
                return float('-inf'), float('inf')

        # ax >= b ==> x >= b/a
        if(A[p][0] != 0):
            value = b[p] / A[p][0]
        else:
            value = b[p]

        # Ukoliko je koeficijent uz x manji od nule treba promeniti znak pa se to odrazava na interval
        if(A[p][0] < 0):
            right_bound = min(right_bound, value)
        else:
            left_bound = max(left_bound, value)

    # Ovaj if povlaci prazan skup, pa to registrujemo kao odsustvo resenja
    if right_bound < left_bound:
        print("Resenje ne postoji")
    else:
        print("Resenje: ")
        str_resenje = ""
        if left_bound == float('-inf'):
            str_resenje += "(-inf, "
        else:
            str_resenje += "[" + left_bound.__str__() + ", "
        if right_bound == float('inf'):
            str_resenje += "inf)"
        else:
            str_resenje += right_bound.__str__() + "]"

        print(str_resenje)

    return left_bound, right_bound

# A = [[1], [-1]]
# b = [2, -3]
#
# left, right = find_intersection(A, b)

def eliminate(A, b):

    n = len(A)
    m = len(A[0])

    elim_index = m-1

    I = []
    J = []
    K = []

    for i in range(0, n):
        if(A[i][elim_index] > 0):
            I.append(i)
        elif(A[i][elim_index] < 0):
            J.append(i)
        else:
            K.append(i)

    #print(f"I = {I}")
    #print(f"J = {J}")
    #print(f"K = {K}")

    new_A = []
    new_b = []

    for i in range(0, len(I)):
        for j in range(0, len(J)):

            new_A.append([])

            for p in range(0, m):
                if(p == elim_index):
                    continue
                x = len(new_A)
                val = (A[I[i]][p] / A[I[i]][elim_index]) - (A[J[j]][p] / A[J[j]][elim_index])
                new_A[x-1].append(val)

            new_b.append(b[I[i]] / A[I[i]][elim_index] - b[J[j]] / A[J[j]][elim_index])

    for k in range(0, len(K)):
        new_A.append([])

        x = len(new_A)

        for p in range(0, m):
            if p == elim_index:
                continue
            new_A[x-1].append(A[K[k]][p])
        new_b.append(b[K[k]])

    if m > 2:
        return eliminate(new_A, new_b)
    else:
        return find_intersection(new_A, new_b)

# A = [[7, 2, -2], [-1, -1, -1], [-2, 3, 1], [5, -1, 1]]
# b = [4, -4, 1, -2]

#left, right = eliminate(A, b)

def is_point_in(A, b, point):

    n = len(A[0])
    m = len(A)

    for i in range(0, m):
        for j in range(0, n):
            b[i] -= A[i][j] * point[j]

        if(b[i] > 0):
            print("Data tacka ne pripada skupu resenja!")
            return

    print("Data tacka pripada skupu resenja")

# A = [[7, 2, -2], [-1, -1, -1], [-2, 3, 1], [5, -1, 1]]
# b = [4, -4, 1, -2]
#point = [1, 4, -2] # DA
point = [1, 2, -3] # DA
#point = [1, 1, 1] # DA
#point = [100, 200, -300] # DA
#point = [0, 0, 2] # NE
#point = [2, 2, 2] # NE
#point = [2, 1, 2] # NE
#point = [0, 0, 2] # NE
#is_point_in(A, b, point)

def transform(A, b, val):

    n = len(A)
    m = len(A[0])

    new_A = []
    new_b = []
    for i in range(0, n):

        #print(f"b[{i}] = {b[i]}")

        res = b[i] - (A[i][0]*val)
        print(res)

        new_b.append(res)

    printVector(new_b)

    for i in range(0, n):
        row = []
        for j in range(0, m):
            if j != 0:
                row.append(A[i][j])
        new_A.append(row)

    return new_A, new_b

#A = [[7, 2, -2], [-1, -1, -1], [-2, 3, 1], [5, -1, 1]]
#b = [4, -4, 1, -2]
#transform(A, b, 0)

def main():

    n = int(input("Unesite broj nejednacina: "))
    m = int(input("Unesite broj promenljivih: "))

    A = []

    for i in range(0, n):

        A.append([])

        for j in range(0, m):

            row = A[i]
            x = int(input("Unesite element matrice: "))
            row.append(x)
        print("Uneli ste red!")

    #printMatrix(A)

    b = []

    for i in range(0, n):
        x = int(input("Unesite element vektora b: "))
        b.append(x)

    #printVector(b)

    while True:

        proms = len(A[0])

        print("Matrica:")
        printMatrix(A)
        print("Vektor:")
        printVector(b)
        print("============================================")

        if proms > 1:
            left, right = eliminate(A, b)
        else:
            left, right = find_intersection(A, b)
            break

        val = int(input("Unesite vrednost za zamenu: "))

        A, b = transform(A, b, val)

main()
