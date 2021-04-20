import math
import numpy as np

def read_input():

    filePath = input("Unesite putanju do fajla: ")
    file = open(filePath, "r")

    lines = file.readlines()

    numOfArticles, backpackVolume = lines[0].split(" ")
    numOfArticles = int(numOfArticles)
    backpackVolume = int(backpackVolume)

    prices = list()
    for x in lines[1].split(" "):
        prices.append(int(x))

    volumes = list()
    for x in lines[2].split(" "):
        volumes.append(int(x))

    return numOfArticles, backpackVolume, prices, volumes

# Funkcija koja vrsi rekonstrukciju resenja
# u slucaju 0-1 ranca
def reconstruct_result_0_1(memo, volumes):

    res = list()

    # Pozicioniramo se u donji desni ugao
    n = len(memo)-1
    m = len(memo[0])-1

    while(n > 0):
        # Ako se element iznad razlikuje od trenutnog
        # Znaci da je on ukljucen u resenje
        if memo[n][m] != memo[n-1][m]:
            # Ukljucujemo ga
            res.append(n-1)
            # Azuriramo kolonu
            m -= volumes[n-1]
        # Azuriramo vrstu
        n -= 1

    res.reverse()
    return res

# Vrsi rekonstrukciju resenja za problem ranca
# u kom mozemo ubacivati vise puta isti predmet
def reconstruct_result(memo, volumes, prices, numOfArticles, backpackVolume):

    vec = np.zeros(numOfArticles)

    n = len(memo) - 1
    m = len(memo[0]) - 1

    price = memo[numOfArticles - 1][backpackVolume]

    while (n > 0):
        if memo[n][m] != memo[n - 1][m]:
            vec[n] += 1
            price -= prices[n]
            m -= volumes[n]
        else:
            n -= 1

    if price > 0:
        vec[0] += math.floor(price / prices[0])

    return vec


def printKnapsackResult(vec, res, method):

    print(f"Metod: {method}")
    print(f"Optimalno resenje je = {res}")
    print(f"Optimalna tacka je = {vec}")


def maximum(vec):

    if len(vec) == 0:
        return 0

    maxi = float('-inf')
    for x in vec:
        if x > maxi:
            maxi = x
    return int(maxi)

# Problem ranca u nazad pri cemu je dozvoljeno uzimanje
# istog predmeta 0 ili vise puta
def UnboundedKnapsack(numOfArticles, backpackVolume, volumes, prices):

    memo = [[0 for i in range(backpackVolume + 1)] for i in range(numOfArticles)]

    for i in range(len(memo[0])):
        memo[0][i] = prices[0] * (math.floor(i / volumes[0]))

    for i in range(1, len(memo)):
        for j in range(len(memo[0])):

            k = math.floor(j / volumes[i])
            vec = []
            for ind in range(k+1):
                vec.append(ind*prices[i] + memo[i-1][j - volumes[i]*ind])

            memo[i][j] = maximum(vec)

    vec = reconstruct_result(memo, volumes, prices, numOfArticles, backpackVolume)

    return memo[numOfArticles-1][backpackVolume], memo, vec


# Problem ranca u napred pri cemu je dozvoljeno uzimanje
# istog predmeta 0 ili vise puta
def UnboundedKnapsackInAdvance(numOfArticles, backpackVolume, volumes, prices):

    memo = [[0 for i in range(backpackVolume+1)] for i in range(numOfArticles)]

    for i in range(len(memo[0])):
        memo[0][i] = prices[0]*(math.floor(i / volumes[0]))

    for i in range(1, len(memo)):
        for j in range(len(memo[0])):

            if volumes[i] <= j:
                memo[i][j] = max(memo[i-1][j], memo[i][j - volumes[i]] + prices[i])
            else:
                memo[i][j] = memo[i-1][j]

    # Sada prelazimo na rekonstrukciju

    vec = reconstruct_result(memo, volumes, prices, numOfArticles, backpackVolume)

    return memo[numOfArticles-1][backpackVolume], memo, vec


# U ovoj implementaciji moguce je uzeti proizvoljan broj
# istih elemenata i ubaciti ih u ranac
def UnboundedKnapsackOptimized(backpackVolume, volumes, prices):

    memo = [0 for i in range(backpackVolume+1)]
    start = min(volumes)

    for i in range(start, backpackVolume+1):
        memo[i] = memo[i-1]
        for k, vk in enumerate(prices):
            if volumes[k] <= i and memo[i] < memo[i - volumes[k]] + vk:
                memo[i] = memo[i - volumes[k]] + vk

    return memo[backpackVolume], memo


# U ovoj implementaciji je moguce svaki predmet uzeti najvise
# jednom i ubaciti ga u ranac
def knapsack_0_1(numOfArticles, backpackVolume, volumes, prices):
    memo = np.zeros((numOfArticles+1, backpackVolume+1))

    for i in range(numOfArticles + 1):
        for vol in range(backpackVolume + 1):
            if i == 0 or vol == 0:
                memo[i][vol] = 0
            elif volumes[i - 1] <= vol:
                memo[i][vol] = max(prices[i - 1] + memo[i - 1][vol - volumes[i - 1]], memo[i - 1][vol])
            else:
                memo[i][vol] = memo[i - 1][vol]

    # Sada imamo tablicu i vrednost
    # Potrebno je rekonstruisati resenje
    vector = reconstruct_result_0_1(memo, volumes)
    result = [0] * numOfArticles
    for val in vector:
        result[val] = 1
    # Ispisujemo rezultat
    print(f"Maksimalna vrednost predmeta koja staje u ranac je: {memo[numOfArticles][backpackVolume]}")
    print(f"Ubaceni su predmeti sa sledecim tezinama: {result}")

    return memo, memo[numOfArticles][backpackVolume]


numOfArticles, backpackVolume, prices, volumes = read_input()
res, memo, vec = UnboundedKnapsackInAdvance(numOfArticles, backpackVolume, volumes, prices)
printKnapsackResult(vec, res, "U napred")
print("----------------------------------------------------")
res, memo, vec = UnboundedKnapsack(numOfArticles, backpackVolume, volumes, prices)
printKnapsackResult(vec, res, "U nazad")
