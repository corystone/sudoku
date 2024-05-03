import sys
from datetime import datetime


class FinishedException(Exception):
    pass


N = 9
sudoku = [0] * N * N
foo = [list(range(1, N + 1)) for _ in range(N * N)]


def reject_box4(cells):
    box = {}
    for x in range(2):
        for y in range(2):
            print(f"x:{x} y:{y}")
            top_left = 2 * N * x + 2 * y
            print(f"top_left: {top_left}")
            if cells[top_left]:
                box_key = (x, y, cells[top_left])
                box[box_key] = True
            if cells[top_left + 1]:
                box_key = (x, y, cells[top_left + 1])
                if box_key in box:
                    return box_key
                box[box_key] = True
            bottom_left = top_left + N
            print(f"bottom_left: {bottom_left}")

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
            print(f"x:{x} y:{y}")
            print(f"top_left: {top_left}")
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
        if key:
            print(f"rejected box: {key} cells: {cells}")

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


def output(P, c):
    print(f"VICTORY! {c}")
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


if __name__ == "__main__":
    start = datetime.now()
    try:
        backtrack(foo, root(foo))
    except FinishedException:
        pass
    print(f"elapsed: {datetime.now() - start}")
