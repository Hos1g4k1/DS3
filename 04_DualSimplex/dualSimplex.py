import numpy as np
import numpy.linalg as LA

# Funkcija za skalarno mnozenje
def scalarMul(a, b):

    res = 0

    n1 = len(a)
    n2 = len(b)
    if(n1 != n2):
        raise IOError

    for i in range(n1):
        res += a[i]*b[i]

    return res

def readInput():

    filePath = input("Unesite putanju do fajla: ")

    file = open(filePath) # Otvara se fajl

    lines = file.readlines() # Citaju se sve linije iz fajla
    br_linija = len(lines)

    br_promenljivih, br_ogranicenja = lines[0].split(" ")
    br_promenljivih = int(br_promenljivih)
    br_ogranicenja = int(br_ogranicenja)

    # print(f"Broj promenljvih = {br_promenljivih}")
    # print(f"Broj ogranicenja = {br_ogranicenja}")

    # Ucitavanje vektora koeficijenata funkcije
    c = np.zeros(br_promenljivih)
    c_s = lines[1].split(" ")
    for i in range(len(c_s)):
        c[i] = float(c_s[i])
    #print(f"c = {c}")

    # Ucitavanje matrice ogranicenja
    A = np.zeros((br_ogranicenja, br_promenljivih))

    for i in range(br_ogranicenja):
        koefs = lines[i+2].split(" ")
        for j in range(br_promenljivih):
            A[i, j] = float(koefs[j])

    #print("Matrica ogranicenja je: ")
    #print(A)

    # Ucitavanje vektora desne strane sistema ogranicenja
    b_koefs = lines[br_linija - 1].split(" ")
    b = []
    for i in range(len(b_koefs)):
        b.append(float(b_koefs[i]))

    return br_promenljivih, br_ogranicenja, A, c.tolist(), b

#readInput()

'''
    Funkcija koja nalazi indeks pivota
'''
def find_pivot(A, c, b_neg_index):

    pivot = None
    max_val = float('-inf')
    for i in range(len(A[0])):
        if(A[b_neg_index][i] < 0):
            val = c[i]/A[b_neg_index][i]
            if val > max_val:
                max_val = val
                pivot = i

    return pivot

'''
    Funkcija za azuriranje simpleks tablice
'''
def updateSystem(A, b, c, F, b_neg_index, pivot):

    n = len(A[0])
    m = len(A)

    coef = 1.0*A[b_neg_index][pivot]

    for i in range(n):
        A[b_neg_index][i] /= coef

    b[b_neg_index] /= coef

    for i in range(m):
        if i == b_neg_index:
            continue

        coef = -A[i][pivot]
        for j in range(n):
            A[i][j] += coef*A[b_neg_index][j]
        b[i] += coef*b[b_neg_index]

    coef = -c[pivot]
    for j in range(n):
        c[j] += coef*A[b_neg_index][j]

    F += coef*b[b_neg_index]

    return A, b, c, F

'''
    Funkcija koja predstavlja dual simpleks metodu za
    resavanje problema linearnog programiranja
'''
def dual_simplex_usingBlend():

    # Ucitavanje podataka
    br_promenljivih, br_ogranicenja, A, c, b = readInput()

    # Pocetna vrednost resenja
    F = 0.0

    n = br_promenljivih - len(c)
    for i in range(n):
        c.append(0)

    iter = 0

    while True:

        print(f"Iteration {iter}")

        print(f"New A:")
        print(np.around(A, 7))
        print("----------------------------------")

        print(f"New b:")
        print(np.around(b, 7))
        print("----------------------------------")

        print(f"New c:")
        print(np.around(c, 7))
        print("----------------------------------")

        print(f"New F:")
        print(np.around(F, 7))
        print("----------------------------------")

        b_neg_index = None

        # Ispitujemo da li postoji negativno b
        for i in range(len(b)):
            if b[i] < 0:
                b_neg_index = i
                break

        # Ukoliko ne postoji to znaci da nemamo dopustivih resenja
        if b_neg_index == None:
            print("Resenje je optimalno!")
            print(f"F = {-np.around(F, 7)}")
            return

        print(f"b[{b_neg_index}] je negativno")

        A_neg_index = None
        # Ukoliko ipak postoji
        # Proveravamo da li su svi koeficijenti u toj vrsti pozitivni
        for i in range(len(A[0])):
            if A[b_neg_index][i] < 0:
                A_neg_index = i
                print(f"A[{b_neg_index}][{i}] je negativno")
                break
        # Ukoliko su svi koeficijenti u toj vrsti pozitivni
        if A_neg_index == None:
            print("Ne postoji resenje!")
            return

        # Ukoliko ipak nisu, trazimo pivot
        pivot = find_pivot(A, c, b_neg_index)
        print(f"Pivot: A[{b_neg_index}][{pivot}]")
        # I azuriramo simpleks tablicu
        A, b, c, F = updateSystem(A, b, c, F, b_neg_index, pivot)

        iter += 1

#dual_simplex_usingBlend()

def dual_simplex():

    # Ucitavanje podataka
    br_promenljivih, br_ogranicenja, A, c, b = readInput()

    # Pocetna vrednost resenja
    F = 0.0

    n = br_promenljivih - len(c)
    for i in range(n):
        c.append(0)

    iter = 0

    while True:

        print(f"Iteration {iter}")

        print(f"New A:")
        print(np.around(A, 7))
        print("----------------------------------")

        print(f"New b:")
        print(np.around(b, 7))
        print("----------------------------------")

        print(f"New c:")
        print(np.around(c, 7))
        print("----------------------------------")

        print(f"New F:")
        print(np.around(F, 7))
        print("----------------------------------")

        b_neg_index = None
        n = len(b)
        # Ispitujemo da li postoji negativno b
        for i in range(len(b)):
            if b[n-i-1] < 0:
                b_neg_index = i
                break

        # Ukoliko ne postoji to znaci da nemamo dopustivih resenja
        if b_neg_index == None:
            print("Resenje je optimalno!")
            print(f"F = {-np.around(F, 7)}")
            return

        print(f"b[{b_neg_index}] je negativno")

        A_neg_index = None
        # Ukoliko ipak postoji
        # Proveravamo da li su svi koeficijenti u toj vrsti pozitivni
        for i in range(len(A[0])):
            if A[b_neg_index][i] < 0:
                A_neg_index = i
                print(f"A[{b_neg_index}][{i}] je negativno")
                break
        # Ukoliko su svi koeficijenti u toj vrsti pozitivni
        if A_neg_index == None:
            print("Ne postoji resenje!")
            return

        # Ukoliko ipak nisu, trazimo pivot
        pivot = find_pivot(A, c, b_neg_index)
        print(f"Pivot: A[{b_neg_index}][{pivot}]")
        # I azuriramo simpleks tablicu
        A, b, c, F = updateSystem(A, b, c, F, b_neg_index, pivot)

        iter += 1

dual_simplex()





