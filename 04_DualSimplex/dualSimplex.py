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

#readInput()

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

def clean(A, P, Q, c, b, E, system, iter):

    #print(f"P = {P}") # Indeksi bazisnih kolona
    #print(f"Q = {Q}") # Indeksi nebazisnih kolona
    #print(f"C = {c}") # Koeficijenti funkcije

    n = len(A)
    m = len(P)

    # Pravimo sistem u*kp = cp, p iz P
    c_b = []

    for i in range(len(P)):
        c_b.append(c[P[i]])

    system = system @ E

    #print("Matrica:")
    #print(system)
    # print("__________________________________________")
    #print("Vektor:")
    #print(c_b)

    # Resavamo formirani sistem da bi nasli u = (u1, ..., um)
    u = LA.solve(system.T, c_b)
    #u = np.dot(LA.inv(system.T), b)

    print(f"u = {np.array(u)}")

    # Nova funkcija je oblika f = u*b suma(q iz Q)(c_q - u*k_q)
    pure_f = []
    for i in range(len(A[0])):
        if i in Q:
            pure_f.append(c[i] - np.dot(u, extact_col(A, i)))
        else:
            pure_f.append(0)

    pure_f.append(np.dot(u, b))
    print(f"pure_f = {np.array(pure_f)}")
    return pure_f, system
'''
    Funkcija koja pronalazi prvi nenegativni clan
'''
def find_first_nonpositive(c, Q):

    for i in Q:
        if c[i] < 0.0:
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
def make_and_solve_system(A, j, P, x0, B):

    # Pravimo sistem
    system = []
    b = []
    for i in range(len(A)):
        for k in range(len(A[0])):
            if(k == j):
                b.append(A[i][j])

    # Resavamo sistem
    #print(system)
    #print(f"j = {j}")
    #print("Sistem za y")
    #print(B)
    #print("Desna strana za y")
    #print(b)

    y = LA.solve(B, b)
    print(f"y = {y}")

    ogr = True

    for v in y:
        if v >= 0:
            ogr = False

    if(ogr):
        print("Funkcija nije ogranice odozdo!")
        return None

    vec = np.zeros(len(x0) + 1)
    vec[P] = y

    # Pravimo parametarsko resenje u dva vektora
    # U vektoru par se nalaze koeficijenti uz t, dakle -y_i
    # U vektoru x0_pom se nalazi x0 pri cemu su ostavljene samo vrednosti na pozicijama iz P

    right = float('inf')
    left = float('-inf')

    for i in P:
        x0_i = x0[i]
        y_i = vec[i]
        # print(f"x0_i = {x0_i}")
        # print(f"y_i = {y_i}")
        if y_i == 0:
            continue

        if (y_i < 0 and x0_i <= 0) or (y_i > 0 and x0_i >= 0):
            right = min(right, x0_i / y_i)
            # print(f"right = {right}")
            # print(f"left = {left}")
            # print("-----------------------------")
        else:
            left = max(left, x0_i / y_i)
            # print(f"right = {right}")
            # print(f"left = {left}")
            # print("-----------------------------")

    if left > right:
        print("Ne postoji t => funkcija nije ogranicena odozdo!")
    else:
        print(f"t = {np.around(right, 13)}")

    return right, vec, y

def find_s_and_update(x0, t, y, j, P, Q):

    s = None # indeks koji trazimo
    for i in P:
        if(y[i] <= 0):
            continue
        val = x0[i] - t*y[i]
        if val == 0:
            s = i
            break

    if s is None:
        print("Izgleda da ovo mora da postoji, nmp")
        exit(1) # KABOOM

    # Azuriramo resenje
    x0_new = np.zeros(len(x0))
    x0_new[j] = t
    for i in P:
        if i != s:
            x0_new[i] = x0[i] - t*y[i]

    # Azuriramo vektor P
    # Veoma je bitno da se j ubaci bas na mesto sa koga izbacujemo s
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

    return x0_new, P_pom, Q_pom, s

'''
    Funkcija koja formira eta matricu
'''
def set_eta(E, y, ind, P):
    l = -1

    for i in range(len(P)):
        if P[i] == ind:
            l = i
            break

    E[:, l] = y

    return E

def revised_simplex():

    br_promenljivih, br_ogranicenja, A, c, b, P, Q, x0 = readInput()

    system = np.eye(len(P))
    E = np.eye(len(P))

    iter = 0

    while True:
        print("-----------------------------------------")
        print(f"ITERACIJA: {iter}")
        print("-----------------------------------------")

        # Cistimo f od bazisnih promenljivih
        pure_f, system_new = clean(np.array(A), P, Q, c, b, E, system, iter)
        # Nalazimo prvo j tako da je c[j] < 0
        j = find_first_nonpositive(pure_f, Q)

        # Ako takvo j ne postoji onda smo nasli optimalno resenje
        if j == None:
            print(f"Resenje je: {np.array(x0)}")
            break
            #return x0
        # Inace pravimo sistem i odredjujemo najvece t
        else:
            t, y, y_c = make_and_solve_system(A, j, P, x0, system_new)

        # Nalazimo koeficijent s na osnovu koga azuriramo P i Q
        x0, new_P, new_Q, s = find_s_and_update(x0, t, y, j, P, Q)

        # Formiramo eta matricu
        E = np.eye(len(P))
        E = set_eta(E, y_c, s, P)

        #system = system @ E

        print("Eta:")
        print(E)

        P = new_P
        Q = new_Q
        # Azuriramo sistem
        system = system_new
        print(f"Trenutno resenje je: {np.array(x0)}")
        #print(f"Novo P je: {P}")
        #print(f"Novo Q je: {Q}")
        iter += 1
        print("_________________________________________")

    res = 0
    for i in range(br_promenljivih):
        res += c[i]*x0[i]

    print(f"min = {np.around(res, 13)}")

revised_simplex()

def dual_simplex():

    br_promenljivih, br_ogranicenja, A, c, b, P, Q, x0 = readInput()

    ind = None

    # Ispitujemo da li postoji negativno b
    for i in range(len(b)):
        if b[i] < 0:
            ind = i
            break

    # Ukoliko ne postoji to znaci da nemamo dopustivih resenja
    if ind == None:
        print("Skup dopustivih resenja je prazan!")
        return

    ind = None

    # Ukoliko ipak postoji
    for i in range(len(b)):
        if b[i] < 0:
            # Proveravamo da li su svi koeficijenti u toj vrsti pozitivni
            for j in range(len(A[0])):
                if A[i][j] < 0:
                    ind = j
                    break

            # Ukoliko jesu to znaci da nemamo resenja
            if ind == None:
                print("Nema resenja ili tako nesto!")
                return

    # Ukoliko smo ipak zakljucili da resenje postoji
    # Trazimo s iz {0, ..., br_ogranicenja-1} takvo da vazi b[s] < 0

    s = None

    for i in range(len(b)):

        if b[i] < 0:
            # Nasli smo s
            s = i

        # Sada trazimo r iz {0, ..., br_promenljivih-1}

        max_coef = float('-inf')

        for j in range(br_promenljivih):

            coef = None
            r = None
            if A[s][j] < 0:
                coef = c[j]/A[s][j]
                if coef > max_coef:
                    max_coef = coef
                    r = j

    # Nasli smo i s i r
    # Sada vrsimo transformacije simpleks tablice

    # S-tu vrstu delimo sa A[s][r]
    for i in range(len(A)):
        for j in range(len(A[0])):
            if i == s:
                A[i][j] /= A[s][r]

    # Ostalim vrstama dodajemo s-tu vrstu pomnozenu odgovarajucim koeficijentom
    # Tako da A[i][r] = 0 za i != s, c[r] = 0
    for i in range(len(A)):
        if i != s:
            for j in range(len(A[0])):
                A[i][j] += A[s][j]














