from collections import deque
import networkx
import matplotlib as plt

graph = {
    1: [2, 3, 11],
    2: [1, 4, 6],
    3: [1, 4],
    4: [2, 3, 6],
    5: [9, 10],
    6: [2, 4, 7, 8],
    7: [6],
    8: [6, 10],
    9: [5, 13],
    10: [5, 8],
    11: [1, 12, 13],
    12: [11, 13],
    13: [9, 11, 12],
}

def bfs_path(graph, s, t):
    visited = {s}
    parent = {s: None}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            break
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    if t not in parent:
        return None
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

def dfs_path(graph, s, t):
    stack = [(s, [s])]
    visited = set()
    while stack:
        u, path = stack.pop()
        if u == t:
            return path
        if u not in visited:
            visited.add(u)
            for v in graph[u]:
                if v not in visited:
                    stack.append((v, path + [v]))
    return None

if __name__ == "__main__":
    start, target = 1, 7
    print("Đường đi BFS từ 1 -> 7 là: ", bfs_path(graph, start, target))