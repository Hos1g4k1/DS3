import numpy as np
import math
from scipy.optimize import linprog
import copy


def readInput():

  filePath = input("Unesite putanju do fajla: ")

  file = open(filePath)  # Otvara se fajl

  lines = file.readlines()  # Citaju se sve linije iz fajla
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
  # print(f"c = {c}")

  # Ucitavanje matrice ogranicenja
  A = np.zeros((br_ogranicenja, br_promenljivih))

  for i in range(br_ogranicenja):
    koefs = lines[i + 2].split(" ")
    for j in range(br_promenljivih):
      A[i, j] = float(koefs[j])

  # print("Matrica ogranicenja je: ")
  # print(A)

  # Ucitavanje vektora desne strane sistema ogranicenja
  b_koefs = lines[br_linija - 1].split(" ")
  b = []
  for i in range(len(b_koefs)):
    b.append(float(b_koefs[i]))

  return A.tolist(), b, c.tolist()
  #return br_promenljivih, br_ogranicenja, A, c.tolist(), b


def isInteger(x):

  x = np.round(x, 8)

  for i in range(len(x)):
    if not x[i].is_integer():
      return i

  return None


def add_constr(A, b, c, val, ind, mode):

  if mode == 'up':
    for i in range(len(A)):
      A[i].append(0)

    new_row = np.zeros(len(A[0]))
    new_row[ind] = 1
    new_row[-1] = -1
    A.append(new_row.tolist())
    b.append(val)
    c.append(0)

    return A, b, c
  else:
    for i in range(len(A)):
      A[i].append(0)

    new_row = np.zeros(len(A[0]))
    new_row[ind] = 1
    new_row[-1] = 1
    A.append(new_row.tolist())
    b.append(val)
    c.append(0)

    return A, b, c


def BnB(A, b, c):

  res = linprog(c=c, A_eq = A, b_eq = b, method='simplex')
  status = res['status']

  if status != 0:
    return None, None

  x = res['x']
  F = res['fun']

  # print(np.round(x, 8))
  # print(F)
  # print()

  ind = isInteger(x)

  if ind is None:
    return x, F

  up = math.ceil(x[ind])
  down = math.floor(x[ind])

  A1, b1, c1 = add_constr(copy.deepcopy(A), copy.deepcopy(b), copy.deepcopy(c), up, ind, 'up')
  A2, b2, c2 = add_constr(copy.deepcopy(A), copy.deepcopy(b), copy.deepcopy(c), down, ind, 'down')

  res1, F1 = BnB(A1, b1, c1)
  res2, F2 = BnB(A2, b2, c2)

  if res1 is None:
    return res2, F2
  elif res2 is None:
    return res1, F1
  else:
    if F1 < F2:
      return res1, F1
    else:
      return res2, F2

def main():

  A, b, c = readInput()

  x, F = BnB(A, b, c)
  if x is None:
    print("Nema resenja")
  else:
    print(np.round(x, 8))
    print(np.round(F, 8))

if __name__ == '__main__':
    main()
