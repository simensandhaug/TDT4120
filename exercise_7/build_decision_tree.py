#!/usr/bin/python3
# coding=utf-8
import random
import uuid
from math import log, ceil


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall utfall.
n_lower = 3
# Høyest mulig antall utfall.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


class TestNode:
    def __init__(self, i):
        self.function = i
        self.true = None
        self.false = None


class LeafNode:
    def __init__(self, name):
        self.name = name
        
from heapq import heapify, heappop, heappush

def build_decision_tree(input_decisions):
    input_decisions = [(d[1], d[0], None, None) for d in input_decisions]
    heapify(input_decisions)
    total_len = len(input_decisions)

    for idx in range(total_len - 1):
        left_node = heappop(input_decisions)
        right_node = heappop(input_decisions)
        combined_freq = left_node[0] + right_node[0]
        heappush(input_decisions, (combined_freq, left_node[1] + right_node[1], left_node, right_node))

    result = {}
    encoding_part("", result, heappop(input_decisions))
    return result

def encoding_part(pre, output, nd):
    if nd[2] or nd[3]:
        encoding_part(pre + "0", output, nd[2])
        encoding_part(pre + "1", output, nd[3])
        return
    output[nd[1]] = pre

def test_expected(rt, input_decisions, func_list):
    e_val = 0
    for name, prob in input_decisions:
        qs = 0
        n = rt
        while isinstance(n, TestNode):
            qs += 1
            if func_list[n.function](name):
                n = n.true
            else:
                n = n.false
        e_val += prob * qs
    return e_val

def build_decision_tree_highscore(input_decisions, tst):
    total_len = len(input_decisions)
    funcs = tst
    tst = list(enumerate(tst))
    p_idx, r_idx = 0, total_len

    optimal_tree = None
    for i, test_func in tst:
        tst_cpy = tst[:]
        tst_cpy.remove((i, test_func))

        start_f = partition_on_test(input_decisions, p_idx, r_idx, test_func)
        if not start_f or start_f == r_idx:
            continue

        rt = TestNode(i)
        rt.true = build_partial_tree_recursive(input_decisions, p_idx, start_f, tst_cpy[:])
        rt.false = build_partial_tree_recursive(input_decisions, start_f, r_idx, tst_cpy)
        optimal_tree = rt if not optimal_tree else min(optimal_tree, rt,
                                                       key=lambda t: test_expected(t, input_decisions, funcs))
    return optimal_tree

def build_partial_tree_recursive(input_decisions, p_idx, r_idx, tst):
    if (r_idx - p_idx) <= 1:
        return LeafNode(input_decisions[p_idx][0])

    total_dec = sum(d[1] for d in input_decisions[p_idx:r_idx])
    sort_func = lambda t: abs(sum(t[1](nm) * freq for nm, freq in input_decisions[p_idx:r_idx]) / total_dec - 0.5)
    tst.sort(key=sort_func)

    i, test_func = tst.pop(0)
    start_f = partition_on_test(input_decisions, p_idx, r_idx, test_func)
    if not start_f or start_f == r_idx:
        return build_partial_tree_recursive(input_decisions, p_idx, r_idx, tst)

    rt = TestNode(i)
    rt.true = build_partial_tree_recursive(input_decisions, p_idx, start_f, tst[:])
    rt.false = build_partial_tree_recursive(input_decisions, start_f, r_idx, tst)
    return rt

def partition_on_test(input_decisions, p_idx, r_idx, test_func):
    i = p_idx
    for j in range(p_idx, r_idx):
        if test_func(input_decisions[j][0]):
            input_decisions[i], input_decisions[j] = input_decisions[j], input_decisions[i]
            i += 1
    return i



# Hardkodete tester på formatet: decisions, tests
tests = [
    ([("a", 0.5), ("b", 0.5)], [lambda x: x == "a"]),
    ([("a", 0.3), ("b", 0.3), ("c", 0.4)], [lambda x: x == "a", lambda x: x == "b"]),
    ([("a", 0.3), ("b", 0.3), ("c", 0.4)], [lambda x: x in ["a", "b"], lambda x: x == "b"]),
    ([("a", 0.3), ("b", 0.3), ("c", 0.4)], [lambda x: x in ["a", "b"], lambda x: x in ["b", "c"]]),
    ([("a", 0.3), ("b", 0.3), ("c", 0.2), ("d", 0.2)], [lambda x: x in ["a", "b"], lambda x: x in ["b", "c"]]),
    ([("a", 0.3), ("b", 0.3), ("c", 0.2), ("d", 0.2)],
     [lambda x: x in ["a", "b"], lambda x: x in ["b", "c"], lambda x: x == "d"]),
]


def test_answer(student, decisions, functions):
    if not isinstance(student, TestNode):
        print("Testen feilet: rotnoden i svaret er ikke en TestNode")
        return -1

    expectance = 0
    for name, prob in decisions:
        questions = 0
        node = student
        while isinstance(node, TestNode):
            questions += 1
            if functions[node.function](name):
                node = node.true
            else:
                node = node.false

        if not isinstance(node, LeafNode):
            print("Testen feilet: noden som ble nådd for {:} er ikke en løvnode".format(name))
            return -1

        if name != node.name:
            print(
                "Testen feilet: Løvnoden som nås av {:} tilhører ikke denne beslutningen".format(
                    name
                )
            )
            return -1

        expectance += prob * questions

    return expectance

def gen_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(max(2, nl), nu)
        decisions = set()
        while len(decisions) < n:
            decisions.add(
                "".join(random.choices("abcdefghijklmnopqrstuvwxyz",
                                       k=ceil(log(n, 26)) + 1))
            )
        prob = [random.randint(1, 10*n) for _ in range(n)]
        scale = sum(prob)
        decisions = [(a, b/scale) for a,b in zip(decisions, prob)]

        def gen_test(var):
            def test(x):
                return x in var
            return test

        names = [a for a,_ in decisions]
        tests = [
            gen_test(random.sample(names, k=random.randint(0, len(names))))
            for _ in range(random.randint(n//3, 3*n))
        ]

        for a in names:
            for b in names:
                if a == b:
                    continue
                if all(test(a) == test(b) for test in tests):
                    subset = random.sample(names, k=random.randint(0, len(names)))
                    if a not in subset:
                        subset.append(a)
                    if b in subset:
                        subset.remove(b)
                    tests.append(gen_test(subset))


        yield decisions, tests


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(random_tests, n_lower, n_upper))

first = True
for test_num, test in enumerate(tests):
    if not first:
        print("-"*50)

    first = False

    tests_string = ""
    for i, check in enumerate(test[1]):
        tests_string += f"T{i + 1}: "
        tests_string += "   ".join(f"{a}={str(check(a)).ljust(5)}" for a, _ in test[0])
        tests_string += "\n"

    print(f"""
Kjører følgende test:
decisions:
{chr(10).join(x + ": " + str(y) for x,y in test[0])}

tests:
{tests_string}
    """)

    student = build_decision_tree_highscore(test[0], test[1])
    result = test_answer(student, test[0], test[1])

    if result != -1:
        print(f"Fikk en forventing på {result}")
    print()