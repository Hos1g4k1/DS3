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


def reconstruct_result(memo, volumes):

    res = list()

    # Pozicioniramo se u donji desni ugao
    n = len(memo)-1
    m = len(memo[0])-1

    while(n > 0):
        # Ako se element iznad razlikuje od trenutnog
        # Znaci da je on ukljucen u resenje
        if memo[n][m] != memo[n-1][m]:
            # Ukljucujemo ga
            res.append(volumes[n-1])
            # Azuriramo kolonu
            m -= volumes[n-1]
        # Azuriramo vrstu
        n -= 1

    res.reverse()
    return res


def knapsack_in_advance(numOfArticles, backpackVolume, volumes, prices):
    memo = [[0 for x in range(backpackVolume + 1)] for x in range(numOfArticles + 1)]

    # Building matrix F[][] from the bottom-up
    for i in range(numOfArticles + 1):
        for vol in range(backpackVolume + 1):
            if i == 0 or vol == 0:
                memo[i][vol] = 0
            elif volumes[i - 1] <= vol:
                memo[i][vol] = max(prices[i - 1] + memo[i - 1][vol - volumes[i - 1]], memo[i - 1][vol])
            else:
                memo[i][vol] = memo[i - 1][vol]

    return memo, memo[numOfArticles][backpackVolume]


numOfArticles = 4
backpackVolume = 9
prices = [3, 4, 5, 2]
volumes = [2, 3, 4, 5]

memo, res = knapsack_in_advance(numOfArticles-1, backpackVolume, volumes, prices)
print(f"Maksimalna vrednost predmeta koja staje u ranac je: {res}")
vector = reconstruct_result(memo, volumes)
print(f"Ubaceni su predmeti sa sledecim tezinama: {vector}")

