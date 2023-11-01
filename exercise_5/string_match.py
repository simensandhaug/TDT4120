# !/usr/bin/python3
# coding=utf-8
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall tegn i dna.
n_lower = 3
# Høyest mulig antall tegn i dna.
n_upper = 100
# Lavest mulig antall tegn i hvert segment.
d_lower = 1
# Høyest mulig antall tegn i hvert segment.
d_upper = 10
# Lavest mulig antall segmenter.
k_lower = 1
# Høyest mulig antall segmenter.
k_upper = 20
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

from collections import deque

def build_ac_automaton(patterns):
    root = Node()
    # Build the trie for the given patterns
    for pattern in patterns:
        node = root
        for char in pattern:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.count += 1
    
    # Build the failure links
    fail_links = {root: None}
    q = deque()
    for child in root.children.values():
        fail_links[child] = root
        q.append(child)

    while q:
        curr = q.popleft()
        for char, child in curr.children.items():
            fail = fail_links[curr]
            while fail and char not in fail.children:
                fail = fail_links[fail]
            fail_links[child] = fail.children[char] if fail else root
            child.count += fail_links[child].count
            q.append(child)

    return root, fail_links

def string_match(dna, segments):
    root, fail_links = build_ac_automaton(segments)
    total_count = 0
    node = root
    for char in dna:
        while node and char not in node.children:
            node = fail_links[node]
        node = node.children[char] if node else root
        total_count += node.count
    return total_count



class Node:
    def __init__(self):
        self.children = {}
        self.count = 0

    def __str__(self):
        return (
            f"{{count: {self.count}, children: {{"
            + ", ".join(
                [f"'{c}': {node}" for c, node in self.children.items()]
            )
            + "}"
        )




# Hardkodete tester på format: ((dna, segments), riktig svar)
tests = [
    (("A", []), 0),
    (("AAAA", ["A"]), 4),
    (("ACTTACTGG", ["A", "ACT", "GG"]), 5),
    (("AAAAAAAAAAAAAAAAAAAA", ["A"]), 20),
    (("AAAAAAAAAAAAAAAAAAAA", ["AA"]), 19),
    (("AAAAAAAAAAAAAAAAAAAA", ["A", "A"]), 40),
    (("AAAAAAAAAAAAAAAAAAAA", ["A", "AA"]), 39),
    (("ABABABABABABABABABAB", ["AB"]), 10),
    (("ABABABABABABABABABAB", ["A", "AB"]), 20),
    (("ABABABABABABABABABAB", ["A", "B"]), 20),
]


# Løser problemet ved bruteforce. Har kjøretid Ω(kn).
def bruteforce_solve(dna, segments):
    counter = 0
    for segment in segments:
        for i in range(len(dna) - len(segment) + 1):
            if dna[i : i + len(segment)] == segment:
                counter += 1
    return counter


def gen_examples(k, nl, nu, dl, du, kl, ku):
    for _ in range(k):
        n = random.randint(nl, nu)
        k_ = random.randint(kl, ku)
        dna = "".join(random.choices("AGTC", k=n))
        segments = [
            "".join(random.choices("AGTC", k=random.randint(dl, du)))
            for _ in range(k_)
        ]
        yield (dna, segments), bruteforce_solve(dna, segments)


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        n_lower,
        n_upper,
        d_lower,
        d_upper,
        k_lower,
        k_upper,
    ))

failed = False

for test_case, answer in tests:
    dna, segments = test_case
    student_answer = string_match(dna, segments[:])
    if student_answer != answer:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for følgende instans:
dna: {dna}
segments: {", ".join(segments)}

Ditt svar: {student_answer}
Riktig svar: {answer}
""")

if not failed:
    print("Koden din fungerte for alle eksempeltestene")