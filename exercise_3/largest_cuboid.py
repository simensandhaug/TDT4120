#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 3
# Høyest mulig antall verdier i generert instans.
# NB: Om denne verdien settes høyt (>30) kan testene ta veldig lang tid.
n_upper = 25
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

def largest_cuboid(matrix):
    memo = {}
    return _calc_max_volume(matrix, 0, 0, len(matrix), len(matrix[0]), memo)


def _calc_max_volume(matrix, r_start, c_start, r_end, c_end, memo, global_min=None):
    cached_result = memo.get((r_start, c_start, r_end, c_end))
    if cached_result is not None:
        return cached_result

    if r_end <= r_start or c_end <= c_start:
        memo[(r_start, c_start, r_end, c_end)] = 0
        return 0

    total_cells = (r_end - r_start) * (c_end - c_start)

    if total_cells == 1:
        cell_value = matrix[r_start][c_start]
        memo[(r_start, c_start, r_end, c_end)] = cell_value
        return cell_value

    min_row, min_col, local_min = _find_local_min(matrix, r_start, c_start, r_end, c_end, global_min)
    
    if min_row is None or min_col is None:
        return 0
    
    if global_min is None:
        global_min = local_min

    opt1 = total_cells * local_min
    opt2 = _calc_max_volume(matrix, r_start, c_start, min_row, c_end, memo, global_min=global_min)
    opt3 = _calc_max_volume(matrix, r_start, c_start, r_end, min_col, memo, global_min=global_min)
    opt4 = _calc_max_volume(matrix, min_row + 1, c_start, r_end, c_end, memo, global_min=global_min)

    max_volume = max(opt1, opt2, opt3, opt4)
    memo[(r_start, c_start, r_end, c_end)] = max_volume
    return max_volume


def _find_local_min(matrix, r_start, c_start, r_end, c_end, global_min):
    local_min = float("inf")
    min_row, min_col = None, None
    for row in range(r_start, r_end):
        for col in range(c_start, c_end):
            cell_value = matrix[row][col]
            if cell_value < local_min:
                if cell_value == global_min:
                    return row, col, global_min
                
                local_min = cell_value
                min_row, min_col = row, col

    return min_row, min_col, local_min



# Hardkodete tester
tests = [
    [[1]],
    [[1, 1], [2, 1]],
    [[1, 1], [5, 1]],
    [[0, 0], [0, 0]],
    [[10, 0], [0, 10]],
    [[10, 6], [5, 10]],
    [[100, 100], [40, 55]],
]


def generate_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        yield [random.choices(range(5*n), k=n) for _ in range(n)]


# Treg bruteforce løsning for å finne løsnings for tilfeldig genererte tester.
def bruteforce_largest_cuboid(x):
    A = 0
    for B in range(len(x)):
        for C in range(len(x[0])):
            for D in range(B, len(x)):
                for E in range(C, len(x[0])):
                    h = min(min(y[C:E + 1]) for y in x[B:D+1])
                    A = max(A, (D - B + 1) * (E - C + 1) * h)
    return A


if generate_random_tests:
    if seed:
        random.seed(seed)

    tests.extend(generate_examples(random_tests, n_lower, n_upper))

failed = False
for x in tests:
    student = largest_cuboid([y[:] for y in x])
    answer = bruteforce_largest_cuboid(x)
    if student != answer:
        if failed:
            print("-"*50)

        failed = True

        print(f"""
Koden ga feil svar for følgende instans:
x: {x}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")