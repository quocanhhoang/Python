import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class FleuryGraph:
    def __init__(self, edges):
        self.graph = defaultdict(list)
        for u, v in edges:
            self.add_edge(u, v)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def remove_edge(self, u, v):
        self.graph[u].remove(v)
        self.graph[v].remove(u)

    def dfs_count(self, v, visited):
        visited[v] = True
        count = 1
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                count += self.dfs_count(neighbor, visited)
        return count

    def is_valid_next_edge(self, u, v):
        if len(self.graph[u]) == 1:
            return True
        visited = {node: False for node in self.graph}
        count1 = self.dfs_count(u, visited)

        self.remove_edge(u, v)
        visited = {node: False for node in self.graph}
        count2 = self.dfs_count(u, visited)
        self.add_edge(u, v)

        return count1 == count2

    def fleury(self, start):
        path = [start]
        current = start

        while True:
            if not self.graph[current]:
                break  # Không còn cạnh nào để đi từ đỉnh hiện tại

            found = False
            for neighbor in self.graph[current]:
                if self.is_valid_next_edge(current, neighbor):
                    print(f"→ Đi từ {current} đến {neighbor}")
                    path.append(neighbor)
                    self.remove_edge(current, neighbor)
                    current = neighbor
                    found = True
                    break

            if not found:
                print(f"⚠ Không tìm được cạnh hợp lệ từ {current}. Dừng lại.")
                break

        return path
def check_euler(graph):
    odd_degree = [node for node in graph if len(graph[node]) % 2 == 1]
    if len(odd_degree) == 0:
        return "Chu trình Euler"
    elif len(odd_degree) == 2:
        return "Đường đi Euler"
    else:
        return "Không có đường/chu trình Euler"

# Tạo đồ thị
G = nx.Graph()
# Thêm các cạnh
edges = [
    ('a', 'b'),
    ('a', 'e'),
    ('b', 'c'),
    ('b', 'd'),
    ('c', 'd'),
    ('c', 'e')
]

G.add_edges_from(edges)
fleury_graph = FleuryGraph(edges)
eulerian_path = fleury_graph.fleury('a')
print("Chu trình Euler:", ' → '.join(eulerian_path))

# Vẽ đồ thị
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=14, edge_color='gray', width=2)
plt.title("Đồ thị từ ảnh", fontsize=16)
plt.axis('off')
plt.show()