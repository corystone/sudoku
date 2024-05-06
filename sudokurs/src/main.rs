use std::time::Instant;

const SQRTN: usize = 2;
const N: usize = 4;
const Nu8: u8 = 4;
const N2: usize = 16;
const N2u8: u8 = 16;

const sudoku: [u8; N2] = [
    1, 2, 0, 0,
    0, 1, 2, 0,
    0, 0, 1, 0,
    0, 0, 0, 0,
];

//const sudoku: [u8; 81]  = [
//    0,0,0,0,0,0,0,0,0,
//    8,6,0,0,5,0,0,3,4,
//    0,2,0,1,0,4,0,6,0,
//    0,5,9,0,0,0,1,4,0,
//    2,0,7,0,0,0,3,0,9,
//    0,8,6,0,0,0,2,5,0,
//    0,4,0,3,0,2,0,9,0,
//    5,7,0,0,8,0,0,2,1,
//    0,0,0,0,0,0,0,0,0,
//];

fn get_constraints(s: &[u8; N2]) -> [Vec<u8>; N2]{
    let mut constraints: [Vec<u8>; N2] = core::array::from_fn(|_| Vec::new());
    for constraint in constraints.iter_mut() {
        for i in 1u8..=Nu8 {
            constraint.push(i);
        }
    }   
    for (i, cell) in s.iter().enumerate() {
        if *cell > 0u8 {
            constraints[i] = vec![*cell]
        }
    }
    constraints
}

fn get_col(index: usize) -> usize {
    index % N
}

fn get_row(index: usize) -> usize {
    index / N
}

fn prune_row(P: &mut[Vec<u8>; N2], row: usize, val: u8) {
    let s = row * N;
    let e = s + N;

    for index in s..e {
    //for (index, cell) in P[s..e].iter_mut().enumerate() {
        let cell = &mut P[index];
        if cell.len() > 1 {
            if cell.contains(&val) {
                cell.retain(|x| *x != val);
                //println!("row removed {val} from cell: {:?} at index: {index}", cell);
            }
        }
    }

}

fn prune_col(P: &mut[Vec<u8>; N2], col: usize, val: u8) {
    let s = col;
    let e = N * N;

    for index in (s..e).step_by(N) {
        let cell = &mut P[index];
        if cell.len() > 1 {
            if cell.contains(&val) {
                cell.retain(|x| *x != val);
                //println!("col removed {val} from cell: {:?} at index: {index}", cell);
            }
        }
    }
}

fn get_box_for_index(index: usize) -> usize {
    let row = index / N;
    let col = index % N;
    let box_row = row / SQRTN;
    let box_col = col / SQRTN;

    box_row * SQRTN + box_col
}

fn prune_box(P: &mut[Vec<u8>; N2], index: usize, val: u8) {
    let which = get_box_for_index(index);

    //let mut thebox: Vec<u8> = vec![];

    let top_left = (which / SQRTN) * SQRTN * N + (which % SQRTN * SQRTN);

    for row in 0..SQRTN {
        for col in 0..SQRTN {
            let index = top_left + col + (row * N);
            let cell = &mut P[index];
            if cell.len() > 1 {
                if cell.contains(&val) {
                    cell.retain(|x| *x != val);
                    //println!("box removed {val} from cell: {:?} at index: {index}", cell);
                }
            }
        }
    }
//            val = cells[index]
//            if val:
//                if val in box:
//                    return True
//                box[val] = True
}
//def prune_box(P, index, val):
//    if N != 9:
//        return
//    which = get_box_for_index(index)
//    for index in iterate_box_indices(which):
//        cell = P[index]
//        if len(cell) > 1:
//            if val in cell:
//                cell.remove(val)
//                print(f"box {which} removed {val} from cell: {cell}")

fn prune(P: &mut[Vec<u8>; N2]) {
    let mut row_prunes = vec![];
    let mut col_prunes = vec![];
    let mut box_prunes = vec![];
    for (index, cell) in P.iter().enumerate() {
        if cell.len() == 1 {
            let val = cell[0];
            let row = get_row(index);
            let col = get_col(index);
            row_prunes.push((row, val));
            col_prunes.push((col, val));
            box_prunes.push((index, val));
        }
    }
    //println!("prunes: col: {:?} row: {:?}, box: {:?}", row_prunes, col_prunes, box_prunes);
    for (row, val) in row_prunes.iter() {
        prune_row(P, *row, *val);
    }
    for (col, val) in col_prunes.iter() {
        prune_col(P, *col, *val);
    }
    for (index, val) in box_prunes.iter() {
        prune_box(P, *index, *val);
    }

}

fn blank_sudoku() -> [u8; N2] {
    let mut blank = [0u8; N2];
    blank
}

fn reject(P: &[Vec<u8>; N2], c: &Vec<u8>) -> bool {
    let mut tmp = blank_sudoku();
    let mut cell = 0;
    for entry in c {
        tmp[cell] = P[cell][usize::from(*entry)];
        cell += 1;
    }

    if c.len() == 0 {
        return false
    }

    let idx = c.len() - 1;
    let row = idx / N;
    let col = idx % N;

    let mut rows = [0u8; N+1];
    for x in row * N..(row + 1) * N {
        let val = tmp[x];
        if val != 0u8 {
            let index = usize::from(val);
            if rows[index] != 0u8 {
                println!("reject row index: {x} val: {val}, tmp: {:?}", tmp);
                return true
            }
            rows[index] = 1u8;
        }
    }

    let mut cols = [0u8; N+1];
    for x in (col..N * N).step_by(N) {
        let val = tmp[x];
        if val != 0u8 {
            let index = usize::from(val);
            if cols[index] != 0u8 {
                println!("reject col index: {x} val: {val}, tmp: {:?}", tmp);
                return true
            }
            cols[index] = 1u8;
        }
    }

    false
}

fn first(P: &[Vec<u8>; N2], c: &mut Vec<u8>) -> Option<Vec<u8>> {
    let mut new_vec = c.clone();
    let cell = c.len();
    if cell < P.len() {
        new_vec.push(0u8);
        return Some(new_vec)
    }
    return None
}

fn next(P: &[Vec<u8>; N2], s: &mut Vec<u8>) -> Vec<u8> {
    let done = vec![];
    let cell = s.len();
    if cell > P.len() || s.len() == 0 {
        return done
    }
    let choices = &P[cell - 1];
    let cur = if let Some(x) = s.pop() {
        x
    } else {
        return done
    };
    if usize::from(cur) == choices.len() - 1 {
        return done
    }
    let mut new_s = s.clone();
    new_s.push(cur+1);
    //println!("NEXT NOT DONE! s: {:?}", new_s);
    new_s
}

fn backtrack(P: &[Vec<u8>; N2], c: &mut Vec<u8>) {
    if reject(P, c) { 
        return
    }
//    else if accept(P, c) {
//        output(P, c)
//    }

    let mut s = if let Some(x) = first(P, c) {
        x
    } else {
        return
    };
    //println!("backtrack, s: {:?}", s);
    while s.len() != 0 {
        backtrack(P, &mut s);
        s = next(P, &mut s);
    }
}

fn main() {
    let start = Instant::now();
    println!("Hello2, world!");
    let duration = start.elapsed();
    let mut constraints = get_constraints(&sudoku);
    prune(&mut constraints);
    println!("{:?}", constraints);

    let mut root: Vec<u8> = vec![];
    backtrack(&constraints, &mut root);

    println!("elapsed: {:?}", duration);
}

// if __name__ == "__main__":
    // start = datetime.now()
    // solved = False
    // constraints = get_constraints(hard_sudoku)
    // prune(constraints)
    // print(constraints)
    // try:
        // backtrack(constraints, root(constraints))
    // except FinishedException:
        // solved = True
    // print(f"elapsed: {datetime.now() - start}")
    // if not solved:
        // print("NO SOLUTION FOUND :(")