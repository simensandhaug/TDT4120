from collections import defaultdict, deque
from math import ceil

import pprint

def bfs(graph, parent, start_node, end_node):
    visited = set()
    queue = deque([start_node])
    visited_add = visited.add  # Local reference to the set.add function
    queue_append = queue.append  # Local reference to the deque.append function
    queue_popleft = queue.popleft  # Local reference to the deque.popleft function
    
    visited_add(start_node)
    
    while queue:
        current_node = queue_popleft()
        
        for neighbour, capacity in graph[current_node].items():
            if neighbour not in visited and capacity > 0:
                queue_append(neighbour)
                visited_add(neighbour)
                parent[neighbour] = current_node
                if neighbour == end_node:
                    return True
    return False


def edmonds_karp(graph, source, sink):
    parent = {}
    max_flow = 0
    
    # Pre-calculate the dict.get methods for each node
    graph_get = {node: graph[node].get for node in graph}
    
    while bfs(graph, parent, source, sink):
        path_flow = float('inf')
        s = sink
        
        # Use the pre-calculated dict.get methods to reduce function call overhead
        while s != source:
            path_flow = min(path_flow, graph_get[parent[s]](s))
            s = parent[s]
        
        max_flow += path_flow
        v = sink
        
        # Again, use the pre-calculated dict.get methods for updating the graph
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    
    return max_flow

def allocate(categories, valuations, n, m):
    """
    Parameters:
        categories: A tuple of tuples (threshold, items) where threshold is the maximum number of items from the set items that can be allocated to a single agent.
        valuations: A tuple of lists where valuations[i] is a list of items that agent i values.
        n (int): The number of agents.
        m (int): The number of items.
        
    Example:
        categories: ((1, (0, 1)), (2, (2, 3))) # Two categories, the first with threshold 1 containing items 0 and 1 and the second with threshold 2 containing items 2 and 3.
        valuations: ([0, 2, 3], [0, 2]) # Two agents, the first values items 0, 2 and 3 and the second values items 0 and 2.
        n: 2
        m: 4
        
    Returns:
        None if there is no proportional allocation (each person gets at least (v_i0 + ... + v_i(m-1))/n items).
        Otherwise returns a list of lists where the i'th list contains the items allocated to agent i.
    """
    
    fair_shares = [ceil(len(v) / n) for v in valuations]
    sum_fair_shares = sum(fair_shares)  # Compute once and store it
    
    graph = defaultdict(lambda: defaultdict(int))  # Using nested defaultdicts for automatic 0 initialization
    
    source_node = 'S'
    sink_node = 'T'
    
    # We'll use list comprehensions and in-place updates to minimize overhead
    # Connect source to items with capacity 1
    for i in range(m):
        item_node = f'I_{i}'
        graph[source_node][item_node] = 1
    
    # Pre-calculate nodes and edges to reduce function call overhead in loops
    item_nodes = [f'I_{i}' for i in range(m)]
    category_nodes = [[f'C_{j}_{i}' for i in range(n)] for j in range(len(categories))]
    agent_nodes = [f'A_{i}' for i in range(n)]
    
    # Connect items to category nodes
    for agent in range(n):
        for category_index, (threshold, items) in enumerate(categories):
            for item in valuations[agent]:
                if item in items:
                    graph[item_nodes[item]][category_nodes[category_index][agent]] = 1
                    
            # Connect category nodes to agent nodes
            graph[category_nodes[category_index][agent]][agent_nodes[agent]] = threshold
            
        # Connect agent nodes to sink
        graph[agent_nodes[agent]][sink_node] = fair_shares[agent]
    
    # Call the edmonds_karp algorithm here
    max_flow = edmonds_karp(graph, source_node, sink_node)
        
    if max_flow < sum_fair_shares:
        return None
    
    # Process the flow graph to find the allocation
    allocation = [[] for _ in range(n)]
    for agent in range(n):
        for category_index, (_, items) in enumerate(categories):
            for item in valuations[agent]:
                if item in items:
                    if graph[item_nodes[item]][category_nodes[category_index][agent]] == 0:
                        allocation[agent].append(item)
    
    return allocation
        

test_categories = ((1, (0, 1)), (2, (2, 3)))
test_valuations = ([0, 2, 3], [0, 2])
test_n = 2
test_m = 4

print(allocate(test_categories, test_valuations, test_n, test_m))










#!/usr/bin/python3
# coding=utf-8
from math import ceil
import random
import itertools


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall agenter i generert instans.
agents_lower = 3
# Høyest mulig antall agenter i generert instans.
# NB: Om denne verdien settes høyt (>25) kan det ta veldig lang tid å
# generere testene.
agents_upper = 8
# Laveste mulige antall gjenstander i generert instans.
items_lower = 3
# Høyest mulig antall gjenstander i generert instans.
# NB: Om denne verdien settes høyt (>25) kan det ta veldig lang tid å
# generere testene.
items_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0




# Hardkodete tester på format:
# (kategorier, verdifunksjoner, n, m, eksisterer det en proporsjonal allokasjon)
tests = [
    (((1, (5, )), (2, (0, 1, 2, 3, 4))), ([], [0, 1, 2, 3, 4, 5]), 2, 6, True)
    ,
    (((1, (0, 1)), (2, (2, 3))),
     ([0, 2, 3], [0, 2]),
     2,
     4,
     True,
    ),
    (((1, (0, 1)),),
     ([0, 1], [0, 1]),
     2,
     2,
     True,
    ),
    (((2, (0, 1, 2)),),
     ([0, 1, 2], [0, 1, 2]),
     2,
     3,
     False,
    ),
    (((2, (0, 1, 2, 3)),),
     ([0, 1, 2, 3], [0, 1, 2, 3]),
     2,
     4,
     True,
    ),
    (((2, (0, 1, 2, 3)),),
     ([0, 1, 3], [0, 1, 3]),
     2,
     4,
     False,
    ),
    (((2, (0, 1, 2)), (1, (3,))),
     ([0, 1, 2, 3], [0, 1, 2, 3]),
     2,
     4,
     True,
    ),
    (((2, (0, 1, 2)), (1, (3,))),
     ([0, 1, 3], [0, 1, 3]),
     2,
     4,
     False,
    ),
    (((2, (0, 1, 2)), (1, (3, 5)), (1, (4,))),
     ([1, 2, 4, 5], [1, 2, 4, 5]),
     2,
     6,
     True,
    ),
]


def check_recursive(categories, likes, req, i, remaining):
    if i == len(likes):
        return True

    choices = remaining & likes[i]
    if len(choices) < req[i]:
        return False

    for comb in itertools.combinations(choices, req[i]):
        comb = set(comb)
        for threshold, items in categories:
            if len(comb & set(items)) > threshold:
                break
        else:
            if check_recursive(categories, likes, req, i + 1, remaining - comb):
                return True

    return False


# Treg bruteforce løsning
def bruteforce_solve(categories, valuations, n, m):
    req = [ceil(len(valuation)/n) for valuation in valuations]
    return check_recursive(categories, valuations, req, 0, set(range(m)))


def gen_examples(k, nl, nu, ml, mu):
    for _ in range(k):
        n = random.randint(nl, nu)
        m = random.randint(ml, mu)
        c = random.randint(1, m)

        boundaries = [0] + sorted([random.randint(0, m) for _ in range(c-1)]) + [m]
        categories = []
        items = list(range(m))
        random.shuffle(items)
        for a, b in zip(boundaries, boundaries[1:]):
            category_items = items[a:b]
            categories.append((random.randint(1, max(len(category_items), 1)),
                               tuple(category_items)))
        categories = tuple(categories)

        val_function = lambda L: lambda x: x in L

        valuations = [
                random.sample(items, random.randint(0, m))
                for _ in range(n)
        ]

        exists = bruteforce_solve(categories, valuations, n, m)

        yield categories, valuations, n, m, exists


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        agents_lower,
        agents_upper,
        items_lower,
        items_upper,
    ))

def verify(m, categories, valuations, exists, student):
    if not exists:
        if student is not None:
            return "Du returnert ikke None selv om det ikke finnes en proporsjonal allokasjon."
        return None

    if type(student) != type([]):
        return "Du returnerte ikke en liste."

    if len(student) != len(valuations):
        return "Svaret inneholder ikke nøyaktig en samling med gjenstander for hver agent."

    # Test that each agent has a list as a bundle
    if any(type(bundle) != type([]) for bundle in student):
        return "En av samlingene med gjenstander er ikke en liste."

    # Test type of each item
    if any(type(item) != int for bundle in student for item in bundle):
        return "Du har returnert en gjenstand som ikke finnes."

    # Test that each item in each bundle is an item
    if not all(0 <= item < m for bundle in student for item in bundle):
        return "Du har returnert en gjenstand som ikke finnes."

    # Test that each item appears at most once in each bundle
    if any(len(set(bundle)) < len(bundle) for bundle in student):
        return "En samling inneholder samme gjenstand flere ganger."

    # Test that some item has not been allocated multiple times
    for i in range(len(valuations)):
        for j in range(i + 1, len(valuations)):
            if set(student[i]) & set(student[j]):
                return "Hver gjenstand kan kun gis til en av personene."

    # Test that each agent does not receive more than threshold items from
    # each category multiple items
    for bundle in student:
        for threshold, category in categories:
            if len(set(bundle) & set(category)) > threshold:
                print(threshold, category, bundle)
                return "En samling innholder flere gjenstander fra en kategori enn er lov."

    for valuation, bundle in zip(valuations, student):
        if len(set(valuation) & set(bundle)) < ceil(len(valuation) / len(valuations)):
            return "En person har ikke fått gjenstander med nok verdi."


def format_valuations(valuations, m):
    string = ""
    for i, valuation in enumerate(valuations):
        string += f"    Agent {i}: {valuation}\n"
    return string


# failed = False
# for categories, valuations, n, m, exists in tests:
#     student = allocate(categories, [val[:] for val in valuations], n, m)
#     feedback = verify(m, categories, valuations, exists, student)

#     if feedback is not None:
#         if failed:
#             print("-"*50)
#         failed = True
#         print(f"""
# Koden feilet for følgende instans:
# n: {n}
# m: {m}
# categories: {categories}
# valuations:
# {format_valuations(valuations, m)}
# Ditt svar: {student}
# Feilmelding: {feedback}
# """)

# if not failed:
#     print("Koden ga riktig svar for alle eksempeltestene")