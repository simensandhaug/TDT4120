def max_permutations(M):
    n = len(M)
    visited = [False] * n
    result = set()
    for i in range(n):
        if visited[i]:
            continue
        cycle = []
        node = i
        while not visited[node]:
            visited[node] = True
            cycle.append(node)
            node = M[node]
        if node in cycle:
            result.update(cycle[cycle.index(node):])
    return {student for student in result if M[student] != student}
highscore = True