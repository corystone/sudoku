# These are my sudokus which I’ve put into lists.
# fmt: off
p = [
5,3,0,0,7,0,0,0,0,
6,0,0,1,9,5,0,0,0,
0,9,8,0,0,0,0,6,0,
8,0,0,0,6,0,0,0,3,
4,0,0,8,0,3,0,0,1,
7,0,0,0,2,0,0,0,6,
0,6,0,0,0,0,2,8,0,
0,0,0,4,1,9,0,0,5,
0,0,0,0,8,0,0,7,9]
p_solved = [
3,5,4,1,6,7,8,9,2,
2,6,7,4,8,9,3,5,1,
8,9,1,2,5,3,4,6,7,
6,4,5,3,7,8,1,2,9,
7,1,8,9,2,5,6,3,4,
9,3,2,6,1,4,7,8,5,
1,2,9,7,3,6,5,4,8,
4,8,3,5,9,1,2,7,6,
5,7,6,8,4,2,9,1,3]
# fmt: on


def f(p, c):
    if c == []:
        return [p[0][0]]
    length = len(c)
    if length > 81:
        return None
    value = p[length][0]
    c.append(value)
    return c


def find_next(cell, value):
    index = 0
    for item in cell:
        if item == value:
            if len(cell) <= index + 1:
                return None
            return cell[index + 1]
        index = index + 1


def n(p, c):
    if c == []:
        return None
    value = c[-1]
    length = len(c)
    cell = p[length - 1]
    number = find_next(cell, value)
    if number is None:
        return None
    c[-1] = number
    return c


# This prints the final sudoku solution.
def print_sudoku(s):
    count = 0
    for number in s:
        print(number, end="")
        count = count + 1
        if count == 9:
            print("")
            count = 0


# This generates all the possibilities for a sudoku.
def create_possibilities(sudoku):
    possibilities = []
    for x in sudoku:
        if x == 0:
            possibilities.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        else:
            possibilities.append([x])
    return possibilities


# This is a modified version of the generic backtracking algorithm.
# It’s faster and shorter than the solve function below.
def solve2(p, c):
    if reject(p, c):
        return
    if accept(c):
        pass
    s = f(p, c)
    while s:
        solve2(p, s[:])
        s = n(p, s)


# This looks at the rows for duplicates.
def reject_row(c):
    for row in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        start = row * 9
        end = start + 9
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for index in range(start, end):
            value = c[index]
            if value == 0:
                continue
            if values[value]:
                return True
            values[value] = 1
    return False


# This looks at the columns for duplicates.
def reject_col(c):
    for column in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        start = column
        end = column + 73
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for index in range(start, end, 9):
            value = c[index]
            if value == 0:
                continue
            if values[value]:
                return True
            values[value] = 1
    return False


# This looks at all the boxes for duplicates.
def reject_box(c):
    for box in [
        [0, 1, 2, 9, 10, 11, 18, 19, 20],
        [3, 4, 5, 12, 13, 14, 21, 22, 23],
        [6, 7, 8, 15, 16, 17, 24, 25, 26],
        [
            27,
            28,
            29,
            36,
            37,
            38,
            45,
            46,
            47,
        ],
        [30, 31, 32, 39, 40, 41, 48, 49, 50],
        [33, 34, 35, 42, 43, 44, 51, 52, 53],
        [54, 55, 56, 63, 64, 65, 72, 73, 74],
        [57, 58, 59, 66, 67, 68, 75, 76, 77],
        [60, 61, 61, 69, 70, 71, 78, 79, 80],
    ]:
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for index in box:
            value = c[index]
            if value == 0:
                continue
            else:
                if values[value]:
                    return True
                values[value] = 1
        return False


# This will reject any possibilities that won't work and is called in solve.
def reject(p, c):
    full_c = c[:]
    while len(full_c) < 81:
        full_c.append(0)
    if reject_row(full_c):
        return True
    if reject_col(full_c):
        return True
    if reject_box(full_c):
        return True
    else:
        return False


# If a sudoku passes reject and is complete, it will be accepted.
import sys


def accept(c):
    if 0 in c:
        return False
    if len(c) < 81:
        return False
    if 0 not in c:
        print(f"VICTORY!!!!")
        print(c)
        print_sudoku(c)
        raise sys.exit(0)


possibilities = create_possibilities(p)

print(possibilities)
# solve(possibilities)
solve2(possibilities, [])
