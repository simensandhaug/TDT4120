# !/usr/bin/python3
# coding=utf-8
from itertools import combinations
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall trafokiosker i generert instans.
substations_lower = 3
# Høyest mulig antall trafokiosker generert instans.
# NB: Om dette antallet settes høyt (>8) vil det ta veldig lang tid å kjøre
# testene, da svaret på instansene finnes ved bruteforce.
substations_upper = 8
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


directions = ((0,-1),(0,1),(-1,0),(1,0))
def power_grid(m, n, substations):
    M = [[-1]*n for _ in range(m)]
    ans = 0
    nodes = []
    for i, station in enumerate(substations):
        M[station[0]][station[1]] = i
        nodes.append(Node(station, i))
    edges = 0
    limit = 0
    while edges<len(substations)-1:
        limit+=1
        merges = dict()
        for node in nodes:
            if node.has_next(limit):
                pos = node.get_next()
                for d in directions:
                    new_pos = (pos[0]+d[0], pos[1]+d[1])
                    if in_map(m, n, new_pos):
                        # if M[new_pos[0]][new_pos[1]]==-1:
                        node.exploreList.append(new_pos)
                            # M[new_pos[0]][new_pos[1]] = node.index
                        # elif M[new_pos[0]][new_pos[1]]==node.index:
                        #     continue
                        if M[new_pos[0]][new_pos[1]]>-1:
                            found_node = nodes[M[new_pos[0]][new_pos[1]]]
                            p1 = find(found_node)
                            p2 = find(node)
                            if p1!=p2:
                                t = (min(p1.index, p2.index), max(p1.index, p2.index))
                                if t in merges:
                                    merges[t] = min(merges[t], distance(node.pos, found_node.pos))
                                else:
                                    merges[t] = distance(node.pos, found_node.pos)
        # merge_list = list(merges.items())
        # merge_list.sort(key=lambda x: x[1])
        # print(merge_list)
        for indices in merges:
            if find(nodes[indices[0]])!=find(nodes[indices[1]]):
                ans+=merges[indices]
                union(nodes[indices[0]], nodes[indices[1]])
                edges+=1
    # print()
    return ans
def distance(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])        

def in_map(m, n, pos):
    return pos[0]>=0 and pos[1]>=0 and pos[0]<m and pos[1]<n

def union(node1, node2):
    n1 = find(node1)
    n2 = find(node2)
    if(n1.rank>n2.rank):
        n2.parent = n1
    else:
        n1.parent = n2
        if n1.rank==n2.rank:
            n2.rank+=1

def find(node):
    if node.parent == None:
        return node
    node.parent = find(node.parent)
    return node.parent

class Node:
    def __init__(self, pos, index):
        self.exploreIndex = 0
        self.exploreList = [pos]
        self.pos = pos
        self.index = index
        self.parent = None
        self.rank = 0
    def has_next(self, limit):
        return self.exploreIndex<len(self.exploreList) and distance(self.pos, self.exploreList[self.exploreIndex])<=limit
    def get_next(self):
        nxt = self.exploreList[self.exploreIndex]
        self.exploreIndex+=1
        return nxt

    
# Hardkodete instanser på format: (m, n, substations)
tests = [
    (2, 2, [(1, 1)]),
    (2, 2, [(0, 0), (1, 1)]),
    (2, 2, [(0, 0), (0, 1), (1, 0)]),
    (2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
    (3, 3, [(0, 2), (2, 0)]),
    (3, 3, [(0, 0), (1, 1), (2, 2)]),
    (3, 3, [(1, 1), (0, 1), (2, 1)]),
    (3, 3, [(1, 2)]),
    (3, 3, [(2, 0), (1, 1), (0, 1)]),
    (2, 3, [(1, 1)]),
    (2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]),
    (2, 2, [(0, 1), (1, 0), (1, 1), (0, 0)]),
    (3, 3, [(0, 1), (0, 2), (2, 1), (2, 2)]),
    (3, 3, [(0, 1), (0, 2), (1, 2), (2, 1)]),
    (2, 3, [(1, 0), (1, 1), (0, 2)]),
    (2, 3, [(1, 0)]),
    (3, 2, [(1, 0), (2, 1), (0, 0)]),
    (3, 3, [(0, 1), (1, 1), (2, 1), (0, 0)]),
    (3, 3, [(0, 2)]),
]


def gen_examples(substations_lower, substations_upper, k):
    for _ in range(k):
        n, m = random.randint(3, 50), random.randint(3, 50)
        s = random.randint(substations_lower, min(substations_upper, n * m))
        substations = set()
        while len(substations) < s:
            substations.add((
                random.randint(0, m - 1),
                random.randint(0, n - 1)
            ))
        substations = list(substations)

        yield (m, n, substations)

def get_answer(m, n, substations):
    # Finner løsningen på problemet ved bruteforce.
    # NB: Bruker minst noen minutter hvis det er 10+ substations
    s = len(substations)
    if s <= 1:
        return 0

    E = [(i, j) for i in range(0, s - 1) for j in range(i + 1, s)]
    def visit(S, v, ST):
        if v in S:
            return
        S.add(v)
        for (a, b) in ST:
            if a == v:
                visit(S, b, ST)
            if b == v:
                visit(S, a, ST)

    solution = float("inf")
    for ST in combinations(E, s - 1):
        S = set()
        visit(S, 0, ST)
        if len(S) != s:
            continue

        answer = 0
        for (a, b) in ST:
            answer += max(substations[a][0], substations[b][0])
            answer -= min(substations[a][0], substations[b][0])
            answer += max(substations[a][1], substations[b][1])
            answer -= min(substations[a][1], substations[b][1])
        if answer < solution:
            solution = answer

    return solution

if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        substations_lower,
        substations_upper,
        random_tests
    ))

failed = False
for m, n, substations in tests:
    answer = get_answer(m, n, substations)
    student = power_grid(m, n, substations)
    if student != answer:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for følgende instans:
m: {m}
n: {n}
substations: {', '.join(map(str, substations))}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
