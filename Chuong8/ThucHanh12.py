def dfs_path(graph, s, t):
    visited = set()
    path = []
    def dfs(u):
        # Đánh dấu và thêm vào đường đi
        visited.add(u)
        path.append(u)
        # Nếu tìm thấy đích thì return True để dừng
        if u == t:
            return True
        for v in graph[u]:
            if v not in visited:
                if dfs(v):
                    return True
        # Nếu không tìm thấy từ nhánh này thì backtrack
        path.pop()
        return False

    if dfs(s):
        return path
    else:
        return None
def build_graph(edges):
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)  # vì đồ thị vô hướng
    return graph

    
edges = [
    (1, 2), (1, 3), (2, 4), (2, 6), (3, 4), (4, 6),
    (6, 7), (6, 8), (8, 10), (10, 5), (5, 9), (9, 13),
    (13, 12), (13, 11), (12, 11), (11, 1)
]
graph = build_graph(edges)
path = dfs_path(graph, 1, 7)

print("Đường đi từ đỉnh 1 đến 7:", path)
