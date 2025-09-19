def DFS_stack(adj, start=1, visited=None):
    n = len(adj)
    if visited is None:
        visited = [False] * n
    res = []

    stack = [start - 1]  # chỉ số mảng bắt đầu từ 0
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            res.append(v + 1)  # cộng 1 để in ra số đỉnh thực tế
            for i in range(n - 1, -1, -1):  # duyệt từ lớn về nhỏ
                if adj[v][i] == 1 and not visited[i]:
                    stack.append(i)
    return res


def DFS_all(adj, start=1):
    n = len(adj)
    visited = [False] * n
    res_total = []

    # duyệt từ đỉnh start trước
    res_total.extend(DFS_stack(adj, start, visited))

    # duyệt tiếp các thành phần còn lại
    for u in range(1, n + 1):
        if not visited[u - 1]:
            res_total.extend(DFS_stack(adj, u, visited))

    return res_total

def bfs(adj, start=1):
    V = len(adj)
    res = [] # Lưu kết quả duyệt
    s = 0
    # Tạo hàng đợi để quản lý BFS
    from collections import deque
    q = deque()
    # Tạo mảng đánh dấu đỉnh đã thăm
    visited = [False] * V
    visited[s] = True
    q.append(s)
    while q:
      curr = q.popleft()
      res.append(curr)
    # Duyệt tất cả các đỉnh kề của curr
      for x in adj[curr]:
          if not visited[x]:
            visited[x] = True
            q.append(x)
    return res


# ===== Ma trận kề cho 13 đỉnh =====
n = 13
adj = [[0] * n for _ in range(n)]
edges = [
    (1, 2), (1, 3), (1, 11),
    (2, 4), (2, 6),
    (3, 4),
    (4, 5),
    (5, 6), (5, 7), (5, 9),
    (6, 8),
    (7, 10),
    (8, 9),
    (9, 13),
    (11, 12), (11, 13),
    (12, 13)
]

for u, v in edges:
    adj[u - 1][v - 1] = 1
    adj[v - 1][u - 1] = 1

# Chạy DFS
res = DFS_all(adj, 1)
# res = bfs(adj, 1)
print("Thứ tự duyệt BFS từ đỉnh 1:", " ".join(map(str, res)))