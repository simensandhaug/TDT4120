#!/usr/bin/python3
# coding=utf-8
import random
from string import ascii_lowercase


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall strenger i generert instans.
n_strings_lower = 3
# Høyest mulig antall strenger i generert instans.
n_strings_upper = 8
# Laveste mulige antall tegn i hver streng i generert instans.
n_chars_lower = 3
# Høyest mulig antall tegn i hver streng i generert instans.
n_chars_upper = 15
# Antall forskjellige bokstaver som kan brukes i strengene. Må være mellom 1 og
# 26. Plukker de første `n_diff_chars` bokstavene i alfabetet.
n_diff_chars = 5
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

def flexradix(A, n, d):
    buckets = [[] for _ in range(d+1)]
    for name in A:
        buckets[len(name)].append(name)
    min_l = d
    names=[]
    while min_l:
        if buckets[min_l]:
            names = buckets[min_l] + names
        if len(names) > 1:
            names = sort(names, min_l-1)
        min_l -= 1
    return names

def sort(A, i):
    buckets = [[] for _ in range(26)]
    for name in A:
        buckets[97 - ord(name[i])].append(name)
    return [name for bucket in buckets for name in bucket]
            
        
    

# Hardkodete instanser på format: (A, d)
tests = [
    ([], 1),
    (["a"], 1),
    (["a", "b"], 1),
    (["b", "a"], 1),
    (["a", "z"], 1),
    (["z", "a"], 1),
    (["ba", "ab"], 2),
    (["b", "ab"], 2),
    (["ab", "a"], 2),
    (["zb", "za"], 2),
    (["abc", "b"], 3),
    (["xyz", "y"], 3),
    (["abc", "b"], 4),
    (["xyz", "y"], 4),
    (["zyxy", "yxz"], 4),
    (["ab", "aaa"], 3),
    (["abc", "b", "bbbb"], 4),
    (["abcd", "abcd", "bbbb"], 4),
    (["abcd", "wxyz", "bbbb"], 4),
    (["abcd", "wxyz", "bazy"], 4),
    (["ab", "aab", "aaab", "aaaab", "aaaaab"], 6),
    (["a", "b", "c", "babcbababa"], 10),
    (["a", "b", "c", "babcbababa"], 10),
    (["w", "x", "y", "xxyzxyzxyz"], 10),
    (["b", "a", "y", "xxyzxyzxyz"], 10),
    (["jfiqdopvak", "nzvoquirej", "jfibopvmcq"], 10),
]

def gen_examples(k, nsl, nsu, ncl, ncu):
    for _ in range(k):
        strings = [
            "".join(random.choices(
                ascii_lowercase,
                k=random.randint(ncl, ncu)
            )) for _ in range(random.randint(nsl, nsu))
        ]
        yield (strings, max(map(len, strings)))


if generate_random_tests:
    ascii_lowercase = ascii_lowercase[:n_diff_chars]
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        n_strings_lower,
        n_strings_upper,
        n_chars_lower,
        n_chars_upper,
    ))

failed = False
for A, d in tests:
    answer = sorted(A)
    student = flexradix(A[:], len(A), d)
    if student != answer:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")