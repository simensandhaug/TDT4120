#!/usr/bin/python3
# coding=utf-8
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall tall i generert instans.
numbers_lower = 3
# Høyest mulig antall tall i generert instans.
numbers_upper = 8
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


from random import randint
def k_largest(A, n, k):
    if k==0:
        return []
    if k==1:
        return [max(A)]
    qSort(A, n, k)
    return A[n-k:n]

def qSort(A, n, k):
    a, b = 0, n
    while True:
        p = partition(A, a, b-1)
        if(p<n-k):
            a = p
        elif(p>len(A)-k):
            b = p
        else:
            return

def partition(A, p, r):
    rand = randint(p, r)
    x = A[rand]
    A[rand], A[r] = A[r], A[rand]
    i = p-1
    for j in range(p, r):
        if A[j]<=x:
            i+=1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1] 
    return i+1


# Sett med hardkodete tester på format: (A, k)
tests = [
    ([], 0),
    ([1], 0),
    ([1], 1),
    ([1, 2], 1),
    ([-1, -2], 1),
    ([-1, -2, 3], 2),
    ([1, 2, 3], 2),
    ([3, 2, 1], 2),
    ([3, 3, 3, 3], 2),
    ([4, 1, 3, 2, 3], 2),
    ([4, 5, 1, 3, 2, 3], 4),
    ([9, 3, 6, 1, 7, 3, 4, 5], 4),
]

def gen_examples(k, lower, upper):
    for _ in range(k):
        A = [
                random.randint(-50, 50)
                for _ in range(random.randint(lower, upper))
            ]
        yield A, random.randint(0, len(A))


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        numbers_lower,
        numbers_upper,
    ))

failed = False
for A, k in tests:
    answer = sorted(A, reverse=True)[:k][::-1]
    student = k_largest(A[:], len(A), k)

    if type(student) != list:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Metoden må returnere en liste
Ditt svar: {student}
""")
    else:
        student.sort()
        if student != answer:
            if failed:
                print("-"*50)
            failed = True
            print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")