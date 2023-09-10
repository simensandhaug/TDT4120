#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 3
# Høyest mulig antall verdier i generert instans.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 123

# 1: 868 lang

#842
def find_maximum(A):
    c = {}
    if len(A) <= 4:
        return max(A)
    return _find_maximum(A, 0, len(A) - 1, c)
def get(A, i, c):
    if i in c:
        return c[i]
    v = A[i]
    c[i] = v
    return v
def _find_maximum(A, l, h, c):
    if h - l < 2:
        return max(get(A, l, c), get(A, h, c))
    m = (l + h) // 2
    l_val, lm1_val, lp1_val = get(A, l, c), get(A, l - 1, c), get(A, l + 1, c)
    m_val, mp1_val = get(A, m, c), get(A, m + 1, c)
    if l_val > max(lm1_val, lp1_val):
        return l_val
    elif lm1_val < l_val < lp1_val:
        if m_val < mp1_val and m_val > l_val:
            return _find_maximum(A, m, h, c)
        return _find_maximum(A, l, m, c)
    elif m_val < l_val or m_val < mp1_val:
        return _find_maximum(A, m, h, c)
    return _find_maximum(A, l, m, c)
highscore = True


# Hardkodete tester på format: (x, svar)
tests = [
    ([1], 1),
    ([1, 3], 3),
    ([3, 1], 3),
    ([1, 2, 1], 2),
    ([1, 0, 2], 2),
    ([2, 0, 1], 2),
    ([0, 2, 1], 2),
    ([0, 1, 2], 2),
    ([2, 1, 0], 2),
    ([2, 3, 1, 0], 3),
    ([2, 3, 4, 1], 4),
    ([2, 1, 3, 4], 4),
    ([4, 2, 1, 3], 4),
    ([8,6,3,1,5,9,12,10],12),
]


# Genererer tilfeldige instanser med svar
def generate_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        x = random.sample(range(5*n), k=n)
        answer = max(x)
        t = x.index(answer)
        x = sorted(x[:t]) + [answer] + sorted(x[t + 1:], reverse=True)
        t = random.randint(0, n)
        x = x[t:] + x[:t]
        yield x, answer


if generate_random_tests:
    if seed:
        random.seed(seed)

    tests.extend(generate_examples(random_tests, n_lower, n_upper))


failed = False
for x, answer in tests:
    student = find_maximum(x[:])
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
    