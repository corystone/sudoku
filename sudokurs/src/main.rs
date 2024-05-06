use std::time::Instant;

// 4
//const SQRTN: usize = 2;
//const N: usize = 4;
//const NU8: u8 = 4;
//const N2: usize = 16;
const SQRTN: usize = 3;
const N: usize = 9;
const NU8: u8 = 9;
const N2: usize = 81;

//const SUDOKU: [u8; N2] = [
//    0, 0, 0, 0,
//    0, 0, 0, 0,
//    0, 0, 0, 0,
//    0, 0, 0, 0,
//];

//const SUDOKU: [u8; N2]  = [
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

const HARD_SUDOKU: [u8; N2] = [
    0,3,0,0,0,0,0,0,0,
    8,0,0,4,7,0,9,0,0,
    1,0,9,0,5,0,8,0,6,
    2,0,0,0,0,5,7,0,0,
    0,0,0,0,0,0,0,0,0,
    0,0,6,1,0,0,0,0,2,
    4,0,3,0,8,0,1,0,9,
    0,0,5,0,4,7,0,0,3,
    0,0,0,0,0,0,0,5,0,
];

// sudoku2
const SUDOKU2: [u8; N2] = [
    8,6,0,0,0,0,0,1,7,
    0,0,5,0,0,0,4,0,0,
    0,0,3,6,0,8,5,0,0,
    0,4,0,0,9,0,0,2,0,
    0,0,1,4,0,7,9,0,0,
    0,5,0,0,1,0,0,7,0,
    0,0,2,8,0,3,6,0,0,
    0,0,7,0,0,0,2,0,0,
    4,9,0,0,0,0,0,3,8,
];

fn get_constraints(s: &[u8; N2]) -> [Vec<u8>; N2]{
    let mut constraints: [Vec<u8>; N2] = core::array::from_fn(|_| Vec::new());
    for constraint in constraints.iter_mut() {
        for i in 1u8..=NU8 {
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

fn prune_row(p: &mut[Vec<u8>; N2], row: usize, val: u8) {
    let s = row * N;
    let e = s + N;

    for index in s..e {
    //for (index, cell) in p[s..e].iter_mut().enumerate() {
        let cell = &mut p[index];
        if cell.len() > 1 {
            if cell.contains(&val) {
                cell.retain(|x| *x != val);
                //println!("row removed {val} from cell: {:?} at index: {index}", cell);
            }
        }
    }

}

fn prune_col(p: &mut[Vec<u8>; N2], col: usize, val: u8) {
    let s = col;
    let e = N * N;

    for index in (s..e).step_by(N) {
        let cell = &mut p[index];
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

fn prune_box(p: &mut[Vec<u8>; N2], index: usize, val: u8) {
    let which = get_box_for_index(index);
    let top_left = (which / SQRTN) * SQRTN * N + (which % SQRTN * SQRTN);

    for row in 0..SQRTN {
        for col in 0..SQRTN {
            let index = top_left + col + (row * N);
            let cell = &mut p[index];
            if cell.len() > 1 {
                if cell.contains(&val) {
                    cell.retain(|x| *x != val);
                    //println!("box removed {val} from cell: {:?} at index: {index}", cell);
                }
            }
        }
    }
}

fn prune(p: &mut[Vec<u8>; N2]) {
    let mut row_prunes = vec![];
    let mut col_prunes = vec![];
    let mut box_prunes = vec![];
    for (index, cell) in p.iter().enumerate() {
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
        prune_row(p, *row, *val);
    }
    for (col, val) in col_prunes.iter() {
        prune_col(p, *col, *val);
    }
    for (index, val) in box_prunes.iter() {
        prune_box(p, *index, *val);
    }

}

fn blank_sudoku() -> [u8; N2] {
    [0u8; N2]
}


fn reject_box(cells: &[u8; N2], index: usize) -> bool {
    let which = get_box_for_index(index);
    let mut box_values = [0u8; N+1];
    let top_left = (which / SQRTN) * SQRTN * N + (which % SQRTN * SQRTN);

    for row in 0..SQRTN {
        for col in 0..SQRTN {
            let index = top_left + col + (row * N);
            let val = cells[index];

            if val != 0u8 {
                let index = usize::from(val);
                if box_values[index] != 0u8 {
                    //println!("reject box: {which} val: {val}, cells: {:?}", cells);
                    return true
                }
                box_values[index] = 1u8;
            }
        }
    }
    false
}

fn reject(p: &[Vec<u8>; N2], c: &Vec<u8>) -> bool {
    let mut tmp = blank_sudoku();
    let mut cell = 0;
    for entry in c {
        tmp[cell] = p[cell][usize::from(*entry)];
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
                //println!("reject row index: {x} val: {val}, tmp: {:?}", tmp);
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
                //println!("reject col index: {x} val: {val}, tmp: {:?}", tmp);
                return true
            }
            cols[index] = 1u8;
        }
    }

    return reject_box(&tmp, idx);
}

fn accept(p: &[Vec<u8>; N2], c: &Vec<u8>) -> bool {
    if c.len() < N {
        return false
    }
    let mut tmp = blank_sudoku();
    let mut cell = 0;
    for entry in c {
        tmp[cell] = p[cell][usize::from(*entry)];
        cell += 1;
    }

    if !tmp.contains(&0u8) {
        return true
    }
    false
}

fn c_to_sudoku(p: &[Vec<u8>; N2], c: &Vec<u8>) -> [u8; N2] {
    let mut tmp = blank_sudoku();
    let mut cell = 0;
    for entry in c {
        tmp[cell] = p[cell][usize::from(*entry)];
        cell += 1;
    }
    tmp
}

fn pprint_sudoku(cells: [u8; N2]) {
    let mut i = 0;
    for y in 0..N {
        for x in 0..N {
            print!("{:?}", cells[i]);
            i += 1;
            if (x + 1) % SQRTN == 0 {
                print!(" ");
            }
        }
        println!("");
        if (y + 1) % SQRTN == 0 {
            println!("");
        }
    }
}

fn output(p: &[Vec<u8>; N2], c: &Vec<u8>) {
    let tmp = c_to_sudoku(p, c);
    println!("VICTORY!!");
    pprint_sudoku(tmp);
}

fn first(p: &[Vec<u8>; N2], c: &mut Vec<u8>) -> Option<Vec<u8>> {
    let mut new_vec = c.clone();
    let cell = c.len();
    if cell < p.len() {
        new_vec.push(0u8);
        return Some(new_vec)
    }
    return None
}

fn next(p: &[Vec<u8>; N2], s: &mut Vec<u8>) -> Vec<u8> {
    let done = vec![];
    let cell = s.len();
    if cell > p.len() || s.len() == 0 {
        return done
    }
    let choices = &p[cell - 1];
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

fn backtrack(p: &[Vec<u8>; N2], c: &mut Vec<u8>) -> bool {
    //println!("backtrack, c: {:?}", c);
    if reject(p, c) { 
        return false
    }
    else if accept(p, c) {
        output(p, c);
        return true
    }

    let mut s = if let Some(x) = first(p, c) {
        x
    } else {
        return false
    };
    while s.len() != 0 {
        //println!("backtrack loop, s: {:?}", s);
        if backtrack(p, &mut s) {
            return true
        }
        s = next(p, &mut s);
    }
    false
}

fn main() {
    let start = Instant::now();
    println!("Hello2, world!");
    let mut constraints = get_constraints(&SUDOKU2);
    prune(&mut constraints);
    println!("CONSTRAINTS: {:?}", constraints);

    let mut root: Vec<u8> = vec![];
    let solved = backtrack(&constraints, &mut root);
    if !solved {
        println!("NO SOLUTION FOUND :(")
    }

    let duration = start.elapsed();
    println!("elapsed: {:?}", duration);
}

