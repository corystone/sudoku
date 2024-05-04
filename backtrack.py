from datetime import datetime


class FinishedException(Exception):
    pass


N = 9
# sudoku = [0] * N * N
# fmt: off

# #121
sudoku = [
    0,0,0,0,0,0,0,0,0,
    8,6,0,0,5,0,0,3,4,
    0,2,0,1,0,4,0,6,0,
    0,5,9,0,0,0,1,4,0,
    2,0,7,0,0,0,3,0,9,
    0,8,6,0,0,0,2,5,0,
    0,4,0,3,0,2,0,9,0,
    5,7,0,0,8,0,0,2,1,
    0,0,0,0,0,0,0,0,0,
]

# 122 faster? due to the first row having constraints maybe?
sudoku2 = [
    8,6,0,0,0,0,0,1,7,
    0,0,5,0,0,0,4,0,0,
    0,0,3,6,0,8,5,0,0,
    0,4,0,0,9,0,0,2,0,
    0,0,1,4,0,7,9,0,0,
    0,5,0,0,1,0,0,7,0,
    0,0,2,8,0,3,6,0,0,
    0,0,7,0,0,0,2,0,0,
    4,9,0,0,0,0,0,3,8,
]

hard_sudoku = [
    0,3,0,0,0,0,0,0,0,
    8,0,0,4,7,0,9,0,0,
    1,0,9,0,5,0,8,0,6,
    2,0,0,0,0,5,7,0,0,
    0,0,0,0,0,0,0,0,0,
    0,0,6,1,0,0,0,0,2,
    4,0,3,0,8,0,1,0,9,
    0,0,5,0,4,7,0,0,3,
    0,0,0,0,0,0,0,5,0,
]

#sudoku = [
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#    0,0,0,0,0,0,0,0,0,
#]
# fmt: on
foo = [list(range(1, N + 1)) for _ in range(N * N)]


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


def iterate_box_indices(which):
    if N != 9:
        return

    box_size = 3
    top_left = (which // box_size) * box_size * N + (which % box_size * box_size)
    for row in range(box_size):
        for col in range(box_size):
            yield top_left + col + (row * N)


def reject_box9(cells):
    box = {}
    for which in range(N):
        box_size = 3
        top_left = (which // box_size) * box_size * N + (which % box_size * box_size)
        for row in range(box_size):
            for col in range(box_size):
                index = top_left + col + (row * N)
                if cells[index]:
                    box_key = (which, cells[index])
                    if box_key in box:
                        return box_key
                    box[box_key] = True
    return False


def reject_box2(cells, index):
    which = get_box_for_index(index)
    box = {}
    box_size = 3
    top_left = (which // box_size) * box_size * N + (which % box_size * box_size)
    for row in range(box_size):
        for col in range(box_size):
            index = top_left + col + (row * N)
            val = cells[index]
            if val:
                if val in box:
                    return True
                box[val] = True
    return False


def reject_box(cells):
    if N == 9:
        return reject_box9(cells)
    elif N == 4:
        return reject_box4(cells)
    return False


def blank_sudoku():
    return [0] * N * N


def reject2(P, c):
    tmp = blank_sudoku()
    cell = 0
    for entry in c:
        tmp[cell] = P[cell][entry]
        cell += 1

    idx = len(c) - 1
    if idx < 0:
        return False

    row = idx // N
    col = idx % N

    rows = {}
    for x in range(row * N, (row + 1) * N):
        val = tmp[x]
        if val:
            if val in rows:
                return True
            rows[val] = True

    cols = {}
    for x in range(col, N * N, N):
        val = tmp[x]
        if val:
            if val in cols:
                return True
            cols[val] = True

    return reject_box2(tmp, idx)


def reject(P, c):
    tmp = blank_sudoku()
    cell = 0
    for entry in c:
        tmp[cell] = P[cell][entry]
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

    tmp = blank_sudoku()
    cell = 0
    for entry in c:
        tmp[cell] = P[cell][entry]
        cell += 1

    if 0 not in tmp:
        return True

    return False


def c_to_sudoku(P, c):
    tmp = blank_sudoku()
    cell = 0
    for entry in c:
        tmp[cell] = P[cell][entry]
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
    pprint_sudoku(c_to_sudoku(P, c))
    raise FinishedException()


def backtrack(P, c):
    if reject2(P, c):
        return
    elif accept(P, c):
        output(P, c)
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


def get_box_for_cell(index):
    for i in range(N):
        if index in list(iterate_box_indices(i)):
            return i
    raise ValueError(f"Couldnt find box for index: {index}")


def get_box_for_index(index):
    row = index // N
    col = index % N

    box_row = row // 3
    box_col = col // 3

    return box_row * 3 + box_col


def prune_box(P, index, val):
    if N != 9:
        return
    which = get_box_for_index(index)
    for index in iterate_box_indices(which):
        cell = P[index]
        if len(cell) > 1:
            if val in cell:
                cell.remove(val)
                print(f"box {which} removed {val} from cell: {cell}")


def prune(P):
    for index, cell in enumerate(P):
        if len(cell) == 1:
            val = cell[0]
            row = get_row(index)
            col = get_col(index)
            # print(f"val: {val} row: {row} col: {col}")
            prune_row(P, row, val)
            prune_col(P, col, val)
            prune_box(P, index, val)
    return P


def get_constraints(sudoku):
    constraints = [list(range(1, N + 1)) for _ in range(N * N)]
    for index, val in enumerate(sudoku):
        if val:
            constraints[index] = [val]
    return constraints


if __name__ == "__main__":
    start = datetime.now()
    solved = False
    constraints = get_constraints(hard_sudoku)
    prune(constraints)
    print(constraints)
    try:
        backtrack(constraints, root(constraints))
    except FinishedException:
        solved = True
    print(f"elapsed: {datetime.now() - start}")
    if not solved:
        print("NO SOLUTION FOUND :(")
