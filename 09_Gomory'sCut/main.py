import numpy as np

from bin.input import input_vars
from bin.make_standardized_form import make_standardized_form
from bin.two_phase_simplex import *
import copy

def decompose(table):

    n = len(table)
    m = len(table[0])

    A = np.zeros((n-1, m-1))
    c = np.zeros(m-1)
    b = np.zeros(n-1)
    F = -1

    for i in range(n):
        for j in range(m):
            if i < n-1 and j < m-1:
                A[i][j] = table[i][j]
            elif i == n-1 and j < m-1:
                c[j] = table[i][j]
            elif i < n-1 and j == m-1:
                b[i] = table[i][j]
            else:
                F = table[i][j]

    return A, b, c, F

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def isInteger(vec):

    vec = np.round(vec, 8)

    for i in range(len(vec)):
        if not vec[i].is_integer():
            return False

    return True

def findFirstNonInt(vec):

    vec = np.round(vec, 8)

    print(f"Vec = {vec}")

    res = list()
    for i in range(len(vec)):
        if vec[i] >= 0:
            res.append(vec[i] - int(vec[i]))
        else:
            res.append(int(abs(vec[i])) + 1 + vec[i])

    print(f"res = {res}")

    ind = -1
    max = float('-inf')
    for i in range(len(res)):
        print(f"res[{i}] = {res[i]}")
        print(f"Max = {max}")
        if res[i] > max:
            max = res[i]
            ind = i

    print(f"Indeks = {ind}")

    return ind

    # for i in range(len(vec)):
    #     if not vec[i].is_integer():
    #         return i

def makeNewConstr(vec, F):

    new_vec = np.zeros(len(vec))

    for i in range(len(vec)):
        if vec[i] >= 0:
            new_vec[i] = vec[i] - int(vec[i])
        else:
            val = int(abs(vec[i]))+1
            new_vec[i] = val + vec[i]

    if F >= 0:
        F = F - int(F)
    else:
        F = int(abs(F)) + 1 + F

    return new_vec, F

def addSlack(tab):

    tab = tab.tolist()

    for x in tab:
        x.append(0)

    return tab

def calculateSol(c, vec):

    F = 0

    for i in range(len(c)):
        F += c[i] * vec[i]

    return -F

def printCut(constr, F):

    print("=========================================")
    print("Cut:")
    print(f"{np.round(constr, 8)} = {np.round(F, 8)}")
    print("=========================================")

def main():
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    # exit()
    n, m, otype, in_c, in_A, sign, in_b = input_vars()
    varNum = len(in_A[0])
    s = System([n, m, otype, in_c, in_A, sign, in_b])
    s.print_problem()
    oproblem = s.problem
    make_standardized_form(s)
    table,x = two_phase_simplex(s, problem=oproblem)

    A, b, c, F = decompose(table)
    first_c = copy.deepcopy(in_c)

    val = -1
    tab = np.vstack((c, A))
    vec = np.hstack((F, b))

    while not isInteger(vec):

        ind = findFirstNonInt(vec)

        newConstr, F = makeNewConstr(tab[ind], vec[ind])
        newConstr = -newConstr
        newConstr = np.hstack((newConstr, np.array([1])))

        printCut(newConstr, -F)

        A = addSlack(A)
        A = np.vstack((A, newConstr))
        b = np.hstack((b, -F))
        c = np.hstack((c, 0))

        signs = list()
        for i in range(len(A)):
            signs.append("=")

        s = System([len(A), len(A[0]), 'min', c, A, signs, b])
        s.print_problem()
        oproblem = s.problem
        make_standardized_form(s)
        table, x = two_phase_simplex(s, problem=oproblem)

        A, b, c, F = decompose(table)

        tab = np.vstack((c, A))
        val = calculateSol(first_c, x)
        vec = np.hstack((val, b))

    finalSol = list()
    for i in range(varNum):
        finalSol.append(x[i])

    print(f"Solution: {np.round(finalSol, 8)}")
    if otype == 'min':
        print(f"Optimal value: {-val}")
    else:
        print(f"Optimal value: {val}")
if __name__ == '__main__':
   main()
