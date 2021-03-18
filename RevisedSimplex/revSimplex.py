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

    print(f"Broj promenljvih = {br_promenljivih}")
    print(f"Broj ogranicenja = {br_ogranicenja}")

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
    b_koefs = lines[br_linija - 4].split(" ")
    b = []
    for i in range(len(b_koefs)):
        b.append(float(b_koefs[i]))

    # Ucitavanje indeksa bazisnih kolona
    P_koefs = lines[br_linija - 3].split(" ")
    P = []
    for i in range(len(P_koefs)):
        P.append(int(P_koefs[i]))
    #print(f"P = {P}")

    # Ucitavanje indeksa nebazisnih kolona
    Q_koefs = lines[br_linija - 2].split(" ")
    Q = []
    for i in range(len(Q_koefs)):
        Q.append(int(Q_koefs[i]))
    #print(f"Q = {Q}")

    # Ucitavanje pocetnog resenja
    x0_koefs = lines[br_linija - 1].split(" ")
    x0 = []
    for i in range(len(x0_koefs)):
        x0.append(float(x0_koefs[i]))
    #print(f"x0 = {x0}")

    return br_promenljivih, br_ogranicenja, A, c, b, P, Q, x0

'''
    Funkcija koja cisti funkciju cilja od bazisnih promenljivih
'''

def extact_col(A, i):

    res = []

    for j in range(len(A)):
        for k in range(len(A[0])):
            if k == i:
                res.append(A[j][k])

    return res

def clean(A, P, Q, c):

    #print(f"P = {P}") # Indeksi bazisnih kolona
    #print(f"Q = {Q}") # Indeksi nebazisnih kolona
    #print(f"C = {c}") # Koeficijenti funkcije

    n = len(A)
    m = len(P)

    # Pravimo sistem u*kp = cp, p iz P
    b = []
    system = np.zeros((n, m))

    for i in range(m):
        for j in range(n):
            system[j][i] = A[j][P[i]]

    for i in range(len(P)):
        b.append(c[P[i]])

    #print("Matrica:")
    #print(system)
    # print("__________________________________________")
    #print("Vektor:")
    #print(b)

    # Resavamo formirani sistem da bi nasli u = (u1, ..., um)
    u = LA.solve(system.T, b)

    print(f"u = {u}")

    # Nova funkcija je oblika f = u*b suma(q iz Q)(c_q - u*k_q)
    pure_f = []
    for i in range(len(A[0])):
        if i in Q:
            pure_f.append(c[i] - np.dot(u, extact_col(A, i)))
        else:
            pure_f.append(0)

    #c.append(np.dot(u, b))
    pure_f.append(np.dot(u, b))
    print(f"pure_f = {pure_f}")
    return pure_f

#A, c, Q, P, x0 = readInput()
#A, c = readInput()
#A = [[1, -1, -1, 3, 1, 0, 0], [5, 1, 3, 8, 0, 1, 0], [-1, 2, 3, -5, 0, 0, 1]]
#b = [1, 55, 3]
#c = [-4, -1, -5, -3, 0, 0, 0]
#x0 = [0, 0, 0, 0, 1, 55, 3]
#P = [4, 5, 6]
#Q = [0, 1, 2, 3]
#A = [[1, 1, 1, 0], [-1, 3, 0, 1]]
#b = [3, 5]
#c = [-1, -2, 0, 0]
#P = [2, 3]
#Q = [0, 1]
#x0 = [0, 0, 3, 5]

#clean(np.array(A), P, Q, c)
'''
    Funkcija koja pronalazi prvi nenegativni clan
'''

def find_first_nonpositive(c, Q):

    for i in Q:
        if c[i] < 0:
            return i

    return None

'''
    Funkcija koja proverava da li je neka vrednost u vektoru
'''

def isIn(i, vec):

    for j in vec:
        if j == i:
            return True

    return False

'''
    Korak K3 u algoritmu. Pravimo sistem (∑i∈P)yiki=kj i resavamo ga po y.
'''

def make_and_solve_system(A, j, P, x0):

    # Pravimo sistem
    system = []
    b = []
    for i in range(len(A)):
        for k in range(len(A[0])):
            if(k == j):
                b.append(A[i][j])

    for i in range(len(A)):
        x = []
        for k in P:
            x.append(A[i][k])
        system.append(x)
    # Resavamo sistem
    #print(system)
    y = LA.solve(system, b)

    print(f"y = {y}")

    ogr = True

    for v in y:
        if v >= 0:
            ogr = False

    if(ogr):
        print("Funkcija nije ogranice odozdo!")
        return None

    vec = np.zeros(len(x0)+1)
    # print(f"y = {y}")
    # print(f"P = {P}")

    vec[P] = y

    # Pravimo parametarsko resenje u dva vektora
    # U vektoru par se nalaze koeficijenti uz t, dakle -y_i
    # U vektoru x0_pom se nalazi x0 pri cemu su ostavljene samo vrednosti na pozicijama iz P
    #par = np.zeros(len(A[0]))
    #x0_pom = np.array(x0)

    right = float('inf')
    left = float('-inf')

    for i in P:
        x0_i = x0[i]
        y_i = vec[i]
        #print(f"x0_i = {x0_i}")
        #print(f"y_i = {y_i}")
        if y_i == 0:
            continue

        if (y_i < 0 and x0_i <= 0) or (y_i > 0 and x0_i >= 0):
            right = min(right, x0_i / y_i)
            #print(f"right = {right}")
            #print(f"left = {left}")
            #print("-----------------------------")
        else:
            left = max(left, x0_i / y_i)
            #print(f"right = {right}")
            #print(f"left = {left}")
            #print("-----------------------------")

    if left > right:
        print("Ne postoji t => funkcija nije ogranicena odozdo!")
    else:
        print(f"t = {right}")

    return right, vec

#make_and_solve_system(A, 0, P, x0)

def find_s_and_update(x0, t, y, j, P, Q):

    s = None # indeks koji trazimo
    y_size = len(y)
    for i in P:

        if(y[i] <= 0):
            continue

        val = x0[i] - t*y[i]
        #print(f"val = {val}")

        if val == 0:
            s = i
            break

    if s is None:
        print("Izgleda da ovo mora da postoji, nmp")
        exit(1)

    # Azuriramo resenje

    for i in range(len(x0)):
        if (isIn(i, P) and i != s):
            x0[i] = x0[i] - t*y[i]
        elif i == j:
            x0[i] = t
        else:
            x0[i] = 0

    # Azuriramo vektor P

    #print(f"Staro P = {P}")
    #print(f"Staro Q = {Q}")
    #print(f"s = {s}")
    #print(f"j = {j}")

    P_pom = []
    for i in range(len(P)):
        if P[i] == s:
            P_pom.append(j)
        else:
            P_pom.append(P[i])

    # Azuriramo vektor Q

    Q_pom = []

    for i in range(len(Q)):
        if Q[i] == j:
            Q_pom.append(s)
        else:
            Q_pom.append(Q[i])

    print(f"P_pom = {P_pom}")
    print(f"Q_pom = {Q_pom}")

    #P_pom = np.sort(P_pom)
    #Q_pom = np.sort(Q_pom)


    return x0, P_pom, Q_pom

def revised_simplex():

    #A, c, Q, P, x0 = readInput()

    #A = [[1, 1, 1, 0], [-1, 3, 0, 1]]
    #b = [3, 5]
    #c = [-1, -2, 0, 0]
    #P = [2, 3]
    #Q = [0, 1]
    #x0 = [0, 0, 3, 5]

    #A = [[1, -1, -1, 3, 1, 0, 0], [5, 1, 3, 8, 0, 1, 0], [-1, 2, 3, -5, 0, 0, 1]]
    #b = [1, 55, 3]
    #c = [-4, -1, -5, -3, 0, 0, 0]
    #P = [4, 5, 6]
    #Q = [0, 1, 2, 3]
    #x0 = [0, 0, 0, 0, 1, 55, 3]

    br_promenljivih, br_ogranicenja, A, c, b, P, Q, x0 = readInput()

    iter = 0

    while True:
        print("Matrica A:")
        print(A)
        #P = np.sort(P)
        #Q = np.sort(Q)

        print(f"ITERACIJA: {iter}")

        # Cistimo f od bazisnih promenljivih
        pure_f = clean(np.array(A), P, Q, c)
        # Nalazimo prvo j tako da je c[j] < 0
        j = find_first_nonpositive(pure_f, Q)

        # Ako takvo j ne postoji onda smo nasli optimalno resenje
        if j == None:
            print(f"Resenje je: {np.array(x0)}")
            break
            #return x0
        # Inace pravimo sistem i odredjujemo najvece t
        else:
            t, y = make_and_solve_system(A, j, P, x0)

        print(f"y = {y}")

        x0, P, Q = find_s_and_update(x0, t, y, j, P, Q)
        print(f"Trenutno resenje je: {x0}")
        print(f"Novo P je: {P}")
        print(f"Novo Q je: {Q}")
        iter += 1
        print("______________________________________")

    res = 0
    for i in range(br_ogranicenja + 1):
        res += c[i] * x0[i]

    print(f"min = {np.around(res, 13)}")

revised_simplex()
