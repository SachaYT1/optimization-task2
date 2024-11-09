import pandas as pd


def findDiff(grid):
    rowDiff = []
    colDiff = []
    for i in range(len(grid)):
        arr = grid[i][:]
        arr.sort()
        rowDiff.append(arr[1] - arr[0])
    col = 0
    while col < len(grid[0]):
        arr = []
        for i in range(len(grid)):
            arr.append(grid[i][col])
        arr.sort()
        col += 1
        colDiff.append(arr[1] - arr[0])
    return rowDiff, colDiff


def findMax(grid):
    rowMax = []
    colMax = []
    for i in range(len(grid)):
        arr = grid[i][:]
        rowMax.append(max(arr))
    col = 0
    while col < len(grid[0]):
        arr = []
        for i in range(len(grid)):
            arr.append(grid[i][col])
        col += 1
        colMax.append(max(arr))
    return rowMax, colMax


def russel_approximation(grid, supply, demand):
    grid = [row[:] for row in grid]
    supply = supply[:]
    demand = demand[:]

    n = len(grid)
    m = len(grid[0])
    INF = 10 ** 6
    ans = 0
    russel_grid = [[0] * len(demand) for _ in range(len(supply))]

    if not isProblemBalanced(supply, demand):
        print("The problem is not balanced!")
        return None, None

    if not isMethodApplicable(grid, supply, demand):
        print("The method is not applicable!")
        return None, None

    while max(supply) != 0 and max(demand) != 0:
        rowMax, colMax = findMax(grid)
        deltaMatrix = [[0] * len(demand) for _ in range(len(supply))]
        row = 0
        col = 0
        minDelta = 10 ** 6
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                deltaMatrix[i][j] = grid[i][j] - (rowMax[i] + colMax[j])
                if deltaMatrix[i][j] < minDelta:
                    minDelta = deltaMatrix[i][j]
                    row = i
                    col = j
        ind = min(supply[row], demand[col])
        ans += ind * grid[row][col]
        russel_grid[row][col] = ind * grid[row][col]
        supply[row] -= ind
        demand[col] -= ind

        if demand[col] == 0:
            for r in range(n):
                grid[r][col] = INF
        else:
            grid[row] = [INF for _ in range(m)]

    return russel_grid, ans


def isProblemBalanced(supply, demand):
    if sum(supply) != sum(demand):
        return False
    return True


def isMethodApplicable(grid, supply, demand):
    flag = True
    if min(supply) < 0:
        flag = False
    if min(demand) < 0:
        flag = False

    for row in grid:
        if min(row) < 0:
            flag = False
        if len(row) != len(demand):
            flag = False
    if len(grid) != len(supply):
        flag = False
    return flag


def vogel_approximation(grid, supply, demand):
    grid = [row[:] for row in grid]
    supply = supply[:]
    demand = demand[:]

    n = len(grid)
    m = len(grid[0])
    INF = 10 ** 6
    ans = 0
    vogel_grid = [[0] * len(demand) for _ in range(len(supply))]

    if not isProblemBalanced(supply, demand):
        print("The problem is not balanced!")
        return None, None

    if not isMethodApplicable(grid, supply, demand):
        print("The method is not applicable!")
        return None, None

    while max(supply) != 0 or max(demand) != 0:
        row, col = findDiff(grid)
        maxi1 = max(row)
        maxi2 = max(col)

        if maxi1 >= maxi2:
            for ind, val in enumerate(row):
                if val == maxi1:
                    mini1 = min(grid[ind])
                    for ind2, val2 in enumerate(grid[ind]):
                        if val2 == mini1:
                            mini2 = min(supply[ind], demand[ind2])
                            ans += mini2 * mini1
                            vogel_grid[ind][ind2] = mini2 * mini1

                            supply[ind] -= mini2
                            demand[ind2] -= mini2

                            if demand[ind2] == 0:
                                for r in range(n):
                                    grid[r][ind2] = INF

                            else:
                                grid[ind] = [INF for _ in range(m)]
                            break
                    break

        else:
            for ind, val in enumerate(col):
                if val == maxi2:
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, grid[j][ind])

                    for ind2 in range(n):
                        val2 = grid[ind2][ind]
                        if val2 == mini1:
                            mini2 = min(supply[ind2], demand[ind])
                            ans += mini2 * mini1

                            vogel_grid[ind2][ind] = mini2 * mini1
                            supply[ind2] -= mini2
                            demand[ind] -= mini2

                            if demand[ind] == 0:
                                for r in range(n):
                                    grid[r][ind] = INF
                            else:
                                grid[ind2] = [INF for _ in range(m)]
                            break
                    break

    return vogel_grid, ans


def nort_west(grid, supply, demand):
    grid = [row[:] for row in grid]
    supply = supply[:]
    demand = demand[:]
    if not isProblemBalanced(supply, demand):
        print("The problem is not balanced!")
        return None, None

    if not isMethodApplicable(grid, supply, demand):
        print("The method is not applicable!")
        return None, None

    startR = 0  # start row
    startC = 0  # start col
    ans = 0
    north_west_grid = [[0] * len(demand) for _ in range(len(supply))]

    while startR != len(grid) and startC != len(grid[0]):

        if supply[startR] <= demand[startC]:
            ans += supply[startR] * grid[startR][startC]
            north_west_grid[startR][startC] = supply[startR] * grid[startR][startC]

            demand[startC] -= supply[startR]
            startR += 1

        else:
            ans += demand[startC] * grid[startR][startC]

            north_west_grid[startR][startC] = demand[startC] * grid[startR][startC]
            supply[startR] -= demand[startC]
            startC += 1
    return north_west_grid, ans


def main():
    print('Input a vector of coefficients of supply - S (3)')
    supply = list(map(int, input().split()))
    print('Input a matrix of coefficients of costs - C (3 x 4)')
    grid = [list(map(int, input().split())) for _ in range(3)]
    print('Input a vector of coefficients of demand - D (4)')
    demand = list(map(int, input().split()))

    df = pd.DataFrame(grid, index=['O1', 'O2', 'O3'], columns=['D1', 'D2', 'D3', 'D4'])

    df['Supply'] = supply

    demand_row = pd.DataFrame([demand + [None]], index=['Demand'], columns=df.columns)
    df = pd.concat([df, demand_row])

    print("Input parameter table")
    print(df)
    print()

    vogel_grid, ans = vogel_approximation(grid, supply, demand)

    if vogel_grid is not None and ans is not None:
        print("The basic feasible solution for Vogel's approximation method is", ans)
        df = pd.DataFrame(vogel_grid, index=['O1', 'O2', 'O3'], columns=['D1', 'D2', 'D3', 'D4'])
        print(df)
        print()

    nort_west_grid, ans = nort_west(grid, supply, demand)

    if vogel_grid is not None and ans is not None:
        print("The basic feasible solution for Nort-West corner method is", ans)
        df = pd.DataFrame(nort_west_grid, index=['O1', 'O2', 'O3'], columns=['D1', 'D2', 'D3', 'D4'])
        print(df)
        print()

    russel_grid, ans = russel_approximation(grid, supply, demand)
    if vogel_grid is not None and ans is not None:
        print("The basic feasible solution for Russel's approximation method is", ans)
        df = pd.DataFrame(russel_grid, index=['O1', 'O2', 'O3'], columns=['D1', 'D2', 'D3', 'D4'])
        print(df)
        print()


if __name__ == '__main__':
    main()
