import  numpy as np
import scipy.linalg as LA

# Funkcija za skalarno mnozenje
def scalarMul(a, b):

    res = 0

    n1 = len(a)
    n2 = len(b)
    if(n1 != n2):
        raise IOError

    for i in range(n1):
        res += a[i]*b[i]


def readInput():

    n = int(input("Unesite broj promenljivih: "))
    print("Unesite funkciju koju optimizujemo:")
    c = []
    # Ucitavanje funkcije cilja
    for i in range(0, n):
        c.append(float(input("Unesite koeficijent: ")))

    A = []
    # Ucitavanje matrice sa koeficijentima jednakosti
    for i in range(n):
        row = []
        for j in range(n):
            x = float(input())
            row.append(x)

        A.append(row)

    k = int(input("Unesite broj bazisnih kolona: "))
    P = []
    # Ucitavanje koeficijenata koji predstavljaju bazisne kolone
    for i in range(k):
        x = float(input())
        P.append(x)

    l = int(input("Unesite broj nebazisnih kolona: "))
    Q = []
    # Ucitavanje koeficijenata koji predstavljaju nebazisne kolone
    for i in range(k):
        x = float(input())
        Q.append(x)

    print("Unesite bazisno moguce resenje: ")
    x0 = []
    # Ucitavanje bazisnog moguceg resenja
    for i in range(n):
        x = float(input())
        x0.append(x)

    return A, c, Q, P, x0

'''
    Funkcija koja cisti funkciju cilja od bazisnih promenljivih
'''

def clean(A, P, Q, c):

    # Pravimo sistem u*kp = cp, p iz P
    system = []
    for i in P:
        system.append(A[i])

    b = []
    for i in P:
        b.append(c[i])

    # Resavamo formirani sistem da bi nasli u = (u1, ..., um)
    u = LA.solve(system, b)

    print(u)

    # Rezultujuca funkcija cilja je
    # f = u*b + suma(cq - u*kq)xq, q iz Q
    #TODO Pogledaj kako se dodaje ovo, moguce je da treba
    #TODO Dodati nule za koeficijente iz P
    new_c = []

    for i in Q:

        koef = scalarMul(u, A[:][i])
        new_c.append(c[i] - koef)

    new_c.append(scalarMul(u, b))

    return new_c