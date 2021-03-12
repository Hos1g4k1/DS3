import  numpy as np
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

    n = int(input("Unesite broj promenljivih: "))
    print("Unesite funkciju koju optimizujemo:")
    c = []
    # Ucitavanje funkcije cilja
    for i in range(0, n):
        c.append(float(input("Unesite koeficijent: ")))

    m = int(input("Unesite broj jednakosti: "))

    print("Unesite matricu koja predstavlja jednakosti: ")
    A = []
    # Ucitavanje matrice sa koeficijentima jednakosti
    for i in range(m):
        row = []
        for j in range(n):
            x = float(input())
            row.append(x)

        A.append(row)

    print("Unesite vektor b: ")
    b = []
    for i in range(m):
        x = float(input())
        b.append(x)

    # k = int(input("Unesite broj bazisnih kolona: "))
    # P = []
    # # Ucitavanje koeficijenata koji predstavljaju bazisne kolone
    # for i in range(k):
    #     x = int(input())
    #     P.append(x)
    #
    # l = int(input("Unesite broj nebazisnih kolona: "))
    # Q = []
    # # Ucitavanje koeficijenata koji predstavljaju nebazisne kolone
    # for i in range(k):
    #     x = int(input())
    #     Q.append(x)
    #
    # print("Unesite bazisno moguce resenje: ")
    # x0 = []
    # # Ucitavanje bazisnog moguceg resenja
    # for i in range(n):
    #     x = float(input())
    #     x0.append(x)
    #
    # return A, c, Q, P, x0
    return A, c
'''
    Funkcija koja cisti funkciju cilja od bazisnih promenljivih
'''

def clean(A, P, Q, c):

    print("P = ", P) # Indeksi bazisnih kolona
    print("C = ", c) # Koeficijenti funkcije

    # Pravimo sistem u*kp = cp, p iz P
    b = []
    n = len(A)
    m = len(P)
    system = np.zeros((n, m))

    for i in range(m):
        for j in range(n):
            system[j][i] = A[j][P[i]]

    for i in range(len(P)):
        b.append(c[P[i]])

    print("Matrica:")
    print(system)
    print("__________________________________________")
    print("Vektor:")
    print(b)

    # Resavamo formirani sistem da bi nasli u = (u1, ..., um)
    u = LA.solve(system, b)
    print(u)

    # Nova funkcija je oblika f = u*b suma(q iz Q)(c_q - u*k_q)
    for i in range(len(Q)):
        c[Q[i]] -= scalarMul(u, A[:, Q[i]])

    print(c)

    c.append(scalarMul(u, b))
    print(c)

    return c

#A, c, Q, P, x0 = readInput()
#A, c = readInput()
#A = [[1, -1, -1, 3, 1, 0, 0], [5, 1, 3, 8, 0, 1, 0], [-1, 2, 3, -5, 0, 0, 1]]
#b = [1, 55, 3]
#c = [-4, -1, -5, -3, 0, 0, 0]
#x0 = [0, 0, 0, 0, 1, 55, 3]
#P = [4, 5, 6]
#Q = [0, 1, 2, 3]
A = [[1, 1, 1, 0], [-1, 3, 0, 1]]
b = [3, 5]
c = [-1, -2, 0, 0]
P = [2, 3]
Q = [0, 1]
x0 = [0, 0, 3, 5]

clean(np.array(A), P, Q, c)
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
    print(system)
    y = LA.solve(system, b)

    print(f"y = {y}")

    ogr = True

    for v in y:
        if v >= 0:
            ogr = False

    if(ogr):
        print("Funkcija nije ogranice odozdo!")
        return None

    # Pravimo parametarsko resenje u dva vektora
    # U vektoru par se nalaze koeficijenti uz t, dakle -y_i
    # U vektoru x0_pom se nalazi x0 pri cemu su ostavljene samo vrednosti na pozicijama iz P
    par = np.zeros(len(A[0]))
    x0_pom = np.array(x0)
    print(x0_pom)

    factor = 0
    for k in range(len(par)):
        if isIn(k, P):
            #print(f"factor = {factor})
            par[k] = -y[factor]
            factor += 1
        elif k == j:
            par[k] = 1
            x0_pom[k] = 0
        else:
            par[k] = 0
            x0_pom[k] = 0

    right = float('inf')
    left = float('-inf')

    # Odredjujemo interval koji zadovoljava prethodni sistem
    # I uzimamo desnu granicu jer je to najvece t
    for k in range(len(x0_pom)):
        if(x0_pom[k] != 0):
            val = x0_pom[k] / par[k]
            if(val >= 0):
                left = max(left, -val)
            else:
                right = min(right, -val)

    print(f"x0_pom = {x0_pom}")
    print(f"par = {par}")

    if left > right:
        print("Ne postoji t => funkcija nije ogranicena odozdo!")
    else:
        print(f"t = {right}")

    return right

make_and_solve_system(A, 0, P, x0)

def revised_simplex():

    #A, c, Q, P, x0 = readInput()

    while True:
        # Cistimo f od bazisnih promenljivih
        c = clean(A, P, c, Q)
        # Nalazimo prvo j tako da je c[j] < 0
        j = find_first_nonpositive(c, Q)

        # Ako takvo j ne postoji onda smo nasli optimalno resenje
        if j == None:
            return x0
        # Inace pravimo sistem i odredjujemo najvece t
        else:
            t, y = make_and_solve_system(A, j, P, x0)



