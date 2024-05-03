from datetime import datetime


class FinishedException(Exception):
    pass


N = 9
sudoku = [0] * N * N
foo = [list(range(1, N + 1)) for _ in range(N * N)]

foo[0] = [8]
foo[1] = [6]
foo[7] = [1]
foo[8] = [7]
foo[11] = [5]
foo[15] = [4]
foo[20] = [3]
foo[21] = [6]
foo[23] = [8]
foo[24] = [5]
foo[28] = [4]
foo[31] = [9]
foo[34] = [2]
foo[38] = [1]
foo[39] = [4]
foo[41] = [7]
foo[42] = [9]
foo[46] = [5]
foo[49] = [1]
foo[52] = [7]
foo[56] = [2]
foo[57] = [8]
foo[59] = [3]
foo[60] = [6]
foo[65] = [7]
foo[69] = [2]
foo[72] = [4]
foo[73] = [9]
foo[79] = [3]
foo[80] = [8]

## fmt: off
# foo = [
# [7,8,9,1],
# [7,8,9],
# [7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],
# [1,2,3,4,5,6,7,8,9],

# ]
## fmt: on


def reject_box4(cells):
    box = {}
    for x in range(2):
        for y in range(2):
            top_left = 2 * N * x + 2 * y
            if cells[top_left]:
                box_key = (x, y, cells[top_left])
                box[box_key] = True
            if cells[top_left + 1]:
                box_key = (x, y, cells[top_left + 1])
                if box_key in box:
                    return box_key
                box[box_key] = True
            bottom_left = top_left + N

            if cells[bottom_left]:
                box_key = (x, y, cells[bottom_left])
                if box_key in box:
                    return box_key
                box[box_key] = True
            if cells[bottom_left + 1]:
                box_key = (x, y, cells[bottom_left + 1])
                if box_key in box:
                    return box_key
    return False


def reject_box9(cells):
    box = {}
    for y in range(3):
        for x in range(3):
            top_left = 3 * N * y + 3 * x
            if cells[top_left]:
                box_key = (x, y, cells[top_left])
                box[box_key] = True
            if cells[top_left + 1]:
                box_key = (x, y, cells[top_left + 1])
                if box_key in box:
                    return box_key
                box[box_key] = True
            if cells[top_left + 2]:
                box_key = (x, y, cells[top_left + 2])
                if box_key in box:
                    return box_key
                box[box_key] = True
            middle_left = top_left + 9
            if cells[middle_left]:
                box_key = (x, y, cells[middle_left])
                if box_key in box:
                    return box_key
                box[box_key] = True
            if cells[middle_left + 1]:
                box_key = (x, y, cells[middle_left + 1])
                if box_key in box:
                    return box_key
                box[box_key] = True
            if cells[middle_left + 2]:
                box_key = (x, y, cells[middle_left + 2])
                if box_key in box:
                    return box_key
                box[box_key] = True
            bottom_left = middle_left + 9
            if cells[bottom_left]:
                box_key = (x, y, cells[bottom_left])
                if box_key in box:
                    return box_key
                box[box_key] = True
            if cells[bottom_left + 1]:
                box_key = (x, y, cells[bottom_left + 1])
                if box_key in box:
                    return box_key
            if cells[bottom_left + 2]:
                box[box_key] = True
                box_key = (x, y, cells[bottom_left + 2])
                if box_key in box:
                    return box_key
    return False


def reject_box(cells):
    if N == 9:
        return reject_box9(cells)
    elif N == 4:
        key = reject_box4(cells)
        # if key:
        # print(f"rejected box: {key} cells: {cells}")
        return key
    return False


def reject(P, c):
    tmp = sudoku.copy()
    cell = 0
    for entry in c:
        tmp[cell] = foo[cell][entry]
        cell += 1

    # print(f"reject: c: {c}, tmp: {tmp}")
    cols = {}
    rows = {}
    for x in range(N):
        for y in range(N):
            row_idx = x * N + y
            if tmp[row_idx]:
                row_key = (x, tmp[row_idx])
                if row_key in rows:
                    # print(f"rejected, row: {row_key}")
                    return True
                rows[row_key] = True
            col_idx = x + N * y
            # print(f"col_idx: {col_idx} x:{x} y:{y} val:{tmp[col_idx]}")
            if tmp[col_idx]:
                col_key = (x, tmp[col_idx])
                if col_key in cols:
                    # print(f"rejected, col: {col_key}")
                    return True
                cols[col_key] = True
    box = reject_box(tmp)
    if box:
        # print(f"rejected box: {box}")
        return True
    return False


def root(P):
    return []


def first(P, c):
    cell = len(c)
    if cell < len(P):
        return c + [0]
    return None


def next(P, s):
    cell = len(s)
    if cell > len(P):
        return None
    choices = P[cell - 1]
    cur = s.pop()
    if cur == len(choices) - 1:
        return None
    return s + [cur + 1]


def accept(P, c):
    if len(c) < N:
        return False

    tmp = sudoku.copy()
    cell = 0
    for entry in c:
        tmp[cell] = foo[cell][entry]
        cell += 1

    if 0 not in tmp:
        return True

    return False


def c_to_sudoku(c):
    tmp = sudoku.copy()
    cell = 0
    for entry in c:
        tmp[cell] = foo[cell][entry]
        cell += 1
    return tmp


def pprint_sudoku(cells):
    i = 0
    for y in range(N):
        for x in range(N):
            print(cells[i], end="")
            i += 1
            if N == 9 and (x == 2 or x == 5):
                print(" ", end="")
        print("")
        if N == 9 and (y == 2 or y == 5):
            print("")


def output(P, c):
    print("VICTORY!")
    pprint_sudoku(c_to_sudoku(c))
    raise FinishedException()


def backtrack(P, c):
    if reject(P, c):
        return
    elif accept(P, c):
        output(P, c)
    # print(f"backtrack c: {c}")
    s = first(P, c)
    while s is not None:
        backtrack(P, s)
        s = next(P, s)


def get_row(index):
    s, e, row = 0, N, 0
    while True:
        if s <= index < e:
            return row
        s += N
        e += N
        row += 1


def get_col(index):
    return index % N


def prune_row(P, row, val):
    print(f"prune_row: {row} val: {val}")
    s = row * N
    e = s + N
    cur = s

    while cur < e:
        cell = P[cur]
        if len(cell) > 1:
            if val in cell:
                cell.remove(val)
                # print(f"removed {val} from cell: {cell}")
        cur += 1


def prune_col(P, col, val):
    print(f"prune_col: {col} val: {val}")
    s = col
    e = N * N

    while s < e:
        cell = P[s]
        if len(cell) > 1:
            if val in cell:
                cell.remove(val)
                # print(f"removed {val} from cell: {cell}")
        s += N


def prune(P):
    for index, cell in enumerate(P):
        if len(cell) == 1:
            val = cell[0]
            row = get_row(index)
            col = get_col(index)
            # print(f"val: {val} row: {row} col: {col}")
            prune_row(P, row, val)
            prune_col(P, col, val)
    return P


if __name__ == "__main__":
    start = datetime.now()
    solved = False
    prune(foo)
    print(foo)
    try:
        backtrack(foo, root(foo))
    except FinishedException:
        solved = True
    print(f"elapsed: {datetime.now() - start}")
    if not solved:
        print("NO SOLUTION FOUND :(")
