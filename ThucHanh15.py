import sys

# Danh sách các đỉnh
nodes = ['A', 'B', 'C', 'D', 'E', 'F']
n = len(nodes)

# Ma trận trọng số mới
graph = [
    [0, 33, 17, 85, 85, 85],  # A
    [33, 0, 18, 20, 85, 85],  # B
    [17, 18, 0, 16, 4, 85],   # C
    [85, 20, 16, 0, 9, 8],    # D
    [85, 85, 4, 9, 0, 14],    # E
    [85, 85, 85, 8, 14, 0]    # F
]

# Bắt đầu từ đỉnh F (chỉ số 5)
start = 5
visited = [False] * n
visited[start] = True

mst_edges = []
total_weight = 0

for _ in range(n - 1):
    min_edge = (None, None)
    min_weight = sys.maxsize

    for u in range(n):
        if visited[u]:
            for v in range(n):
                if not visited[v] and graph[u][v] < min_weight and graph[u][v] != 0:
                    min_edge = (u, v)
                    min_weight = graph[u][v]

    u, v = min_edge
    visited[v] = True
    mst_edges.append((nodes[u], nodes[v], min_weight))
    total_weight += min_weight

# In kết quả
print("Các cạnh trong cây khung nhỏ nhất:")
for edge in mst_edges:
    print(f"{edge[0]} – {edge[1]}: {edge[2]}")

print(f"Tổng trọng số: {total_weight}")