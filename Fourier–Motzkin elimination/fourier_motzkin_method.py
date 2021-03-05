import numpy as np
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
    Funkcija koja kreira string reprezentaciju intervala
'''

def form_interval(left, right):
    resenje = ""
    if left == float('-inf'):
        resenje += "(-inf, "
    else:
        resenje += "[" + left.__str__() + ", "
    if right == float('inf'):
        resenje += "inf)"
    else:
        resenje += right.__str__() + "]"

    return resenje

'''
    Ova funkcija se poziva kada su uklonjenje sve promenljive sem poslednje
    Vrsi se presek svih nejednakosti i vraca se interval
'''

def find_interval(A, b):

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
            if(b[p]*A[p][0] <= 0):
                value = float("-inf")
            elif (b[p]*A[p][0] >= 0):
                value = float("inf")
            #value = b[p]

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
        str_resenje = form_interval(left_bound, right_bound)
        print(str_resenje)

    #return left_bound, right_bound

# A = [[1], [-1]]
# b = [2, -3]
#
# left, right = find_intersection(A, b)

def eliminate(A, b):

    n = len(A) # Broj nejednakosti
    m = len(A[0]) # Broj promenljivih

    elim_index = m-1

    I = [] # Vektor indeksa onih nejednakosti koje ...
    J = [] # Vektor indeksa onih nejednakosti koje ...
    K = [] # Vektor indeksa onih nejednakosti koje ...

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
        return find_interval(new_A, new_b)

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

def reduce(A, b, val):

    n = len(A)
    m = len(A[0])

    new_A = []
    new_b = []
    for i in range(0, n):

        #print(f"b[{i}] = {b[i]}")
        res = b[i] - (A[i][0]*val)
        #print(res)
        new_b.append(res)

    #printVector(new_b)

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

def incorporate_f(A, b, c):

    n = len(b) # Broj nejednacina
    m = len(c) # Broj promenljivih

    if(n == 0):
        return

    for i in range(0, n):

        for j in range(1, m):
            #print("i: ", i)
            #print("j: ", j)
            A[i][j] -= (c[j]/c[0])*A[i][0]

        # Ako imamo nesto tipa f = 3x - y
        # Dobijamo 3x = f + y
        # Pa treba podeliti za 1/3
        A[i][0] *= 1.0 / c[0]

    #print(A)

    return A

def load_matrix(n, m):
    A = []

    for i in range(0, n):
        A.append([])
        for j in range(0, m):
            row = A[i]
            x = int(input("Unesite element matrice: "))
            row.append(x)
        print("Uneli ste red!")
    return A

def load_vector(n):
    b = []

    for i in range(0, n):
        x = int(input("Unesite element vektora b: "))
        b.append(x)

    return b

def fourier_motzkin_elimination():

    n = int(input("Unesite broj nejednacina: "))
    m = int(input("Unesite broj promenljivih: "))

    A = load_matrix(n, m)
    #printMatrix(A)

    b = load_vector(n)
    #printVector(b)

    while True:

        proms = len(A[0])
        # print("Matrica:")
        # printMatrix(A)
        # print("Vektor:")
        # printVector(b)
        # print("============================================")

        if proms > 1:
            eliminate(A, b)
        else:
            find_interval(A, b)
            break

        val = int(input("Unesite vrednost za zamenu: "))

        A, b = reduce(A, b, val)
        print("============================================")

#fourier_motzkin_elimination()

def linear_programming_problem():
    n = int(input("Unesite broj nejednacina: "))
    m = int(input("Unesite broj promenljivih: "))

    # c = [7.75, 8.5]
    # A = [[1.5, 2], [2.25, 1.5]]
    # b = [120, 135]

    c = [5, 7]
    A = [[3, 4], [2, 3]]
    b = [650, 500]

    #A = load_matrix(n, m)
    # printMatrix(A)
    #b = load_vector(n)
    # printVector(b)
    #c = load_vector(m)
    # printVector(c)

    # Transformisemo sistem u oblik
    # a00x1 + a01x2 >= b1
    # a10x1 + a11x2 >= b2
    # a20x1 + a21x2 >= b3
    A = -np.array(A)
    b = -np.array(b)

    # Dodajemo uslove da je svaka od promenljivih >= 0
    # x0 >=0, x1 >= 0, ...
    for i in range(0, n):
        vec = np.zeros(m)
        vec[i] = 1
        A = np.vstack((A, vec))
        b = np.append(b, 0)

    # print("A:")
    # printMatrix(A)
    # print("b:")
    # printVector(b)
    # print("c:")
    # printVector(c)

    A = incorporate_f(A, b, c)
    eliminate(A, b)

linear_programming_problem()