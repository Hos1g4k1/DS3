import numpy as np

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

    m = len(b) # Broj nejednakosti
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

    # Eliminaciju pocinjemo sa desnog kraja
    # Stoga intervale odredjujemo prvo za
    # Najlevlju promenljivu
    elim_index = m-1

    I = [] # Vektor indeksa onih nejednakosti kojima je koeficijent na poziciji elim_indeks > 0
    J = [] # Vektor indeksa onih nejednakosti kojima je koeficijent na poziciji elim_indeks < 0
    K = [] # Vektor indeksa onih nejednakosti kojima je koeficijent na poziciji elim_indeks = 0

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

    # Vrsimo kombinovanje nejedankosti iz skupova I i J
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

    # Nejednakosti iz skupa K prepisujemo
    for k in range(0, len(K)):
        new_A.append([])
        x = len(new_A)
        for p in range(0, m):
            if p == elim_index:
                continue
            new_A[x-1].append(A[K[k]][p])
        new_b.append(b[K[k]])

    # Ukoliko ima 2 ili vise promenljivi
    # Potrebno je nastaviti sa eliminacijom
    # Inace prelazimo na trazenje intervala
    if m > 2:
        return eliminate(new_A, new_b)
    else:
        return find_interval(new_A, new_b)

# A = [[7, 2, -2], [-1, -1, -1], [-2, 3, 1], [5, -1, 1]]
# b = [4, -4, 1, -2]

#left, right = eliminate(A, b)

'''
    Funkcija koja proverava da li data tacka pripada skupu resenja
'''
def is_point_in(A, b, point):

    if ((A @ point >= b).all):
        print("Data tacka pripada skupu resenja!")
    else:
        print("Data tacka ne pripada skupu resenja!")

#TEST PRIMERI
A = [[7, 2, -2], [-1, -1, -1], [-2, 3, 1], [5, -1, 1]]
b = [4, -4, 1, -2]
#point = [1, 4, -2] # DA
point = [1, 2, -3] # DA
#point = [1, 1, 1] # DA
#point = [100, 200, -300] # DA
#point = [0, 0, 2] # NE
#point = [2, 2, 2] # NE
#point = [2, 1, 2] # NE
#point = [0, 0, 2] # NE
is_point_in(np.array(A), np.array(b), np.array(point))

'''
    Funkcija koja uvrstava vrednost za promenljivu u sistem
    i vraca nam novonastali sistem
'''

def substitute(A, b, val):

    n = len(A) # Broj nejednakosti
    m = len(A[0]) # Broj promenljivih

    new_A = []
    new_b = []

    # a1x1 + a2x2 >= b
    # a2x2 >= b - a1x1
    for i in range(0, n):

        #print(f"b[{i}] = {b[i]}")
        res = b[i] - (A[i][0]*val)
        #print(res)
        new_b.append(res)

    #print(new_b)

    # Uvrstili smo prvu promenljivu
    # Koeficijente uz ostale prepisujemo
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

'''
    Funkcija koja uvrstava izrazenu funkciju u sistem
'''

def incorporate_f(A, b, c):

    n = len(b) # Broj nejednacina
    m = len(c) # Broj promenljivih

    if(n == 0):
        return

    #Ako imamo f = x + y i nejednakostx + 2y >= 3
    #Izrazimo x = f - y i zamenimo u drugoj nejednakosti
    #I dobijamo f + y >= 3

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
    #print(A)

    b = load_vector(n)
    #print(b)

    # U petlji konstantno odredjujemo interval za najlevlju promenljivu
    # Eliminisemo je i ponavljamo postupak za preostale promenljive
    # Petlja staje kada dodjemo do sistema nejednacina sa jednom promenljivom
    while True:

        proms = len(A[0])
        # print("Matrica:")
        # print(A)
        # print("Vektor:")
        # print(b)

        if proms > 1:
            eliminate(A, b)
        else:
            find_interval(A, b)
            break

        val = int(input("Unesite vrednost za zamenu: "))

        A, b = substitute(A, b, val)
        print("============================================")

#fourier_motzkin_elimination()

def linear_programming_problem():
    # n = int(input("Unesite broj nejednacina: "))
    # m = int(input("Unesite broj promenljivih: "))

    # A = load_matrix(n, m)
    # print(A)
    # b = load_vector(n)
    # print(b)
    # c = load_vector(m)
    # print(c)

    # c = [7.75, 8.5]
    # A = [[1.5, 2], [2.25, 1.5]]
    # b = [120, 135]
    # n = 2
    # m = 2

    # c = [5, 7]
    # A = [[3, 4], [2, 3]]
    # b = [650, 500]
    # n = 2
    # m = 2

    # Primer iz sveske
    c = [-1, -1]
    A = [[-1, 1], [-0.5, -1]]
    b = [-1, -1]
    n = 2
    m = 2

    # Transformisemo sistem u oblik
    # a00x1 + a01x2 >= b1
    # a10x1 + a11x2 >= b2
    # a20x1 + a21x2 >= b3
    #A = -np.array(A)
    #b = -np.array(b)

    # Dodajemo uslove da je svaka od promenljivih >= 0
    # x0 >=0, x1 >= 0, ...
    for i in range(0, n):
        vec = np.zeros(m)
        vec[i] = 1
        A = np.vstack((A, vec))
        b = np.append(b, 0)

    # print("A:")
    # print(A)
    # print("b:")
    # print(b)
    # print("c:")
    # print(c)

    # Uvrstavamo f u sistem
    A = incorporate_f(A, b, c)
    # I resavamo ga pomocu Furije-Mockin metoda
    eliminate(A, b)

linear_programming_problem()
