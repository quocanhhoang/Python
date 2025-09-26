from functools import cmp_to_key

def comparator(a,b):
    return a[2] - b[2];

def kruskals_mst(V, edges):

    # Sort all edges
    edges = sorted(edges,key=cmp_to_key(comparator))
    
    # Traverse edges in sorted order
    dsu = DSU(V)
    cost = 0
    count = 0
    for x, y, w in edges:
        
        # Make sure that there is no cycle
        if dsu.find(x) != dsu.find(y):
            dsu.union(x, y)
            cost += w
            count += 1
            if count == V - 1:
                break
    return cost
    
# Disjoint set data structure
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        s1 = self.find(x)
        s2 = self.find(y)
        if s1 != s2:
            if self.rank[s1] < self.rank[s2]:
                self.parent[s1] = s2
            elif self.rank[s1] > self.rank[s2]:
                self.parent[s2] = s1
            else:
                self.parent[s2] = s1
                self.rank[s1] += 1
def main():
    V = 8  # Số lượng đỉnh từ hình ảnh
    # Danh sách cạnh từ hình ảnh, chuyển về dạng vô hướng
    raw_edges = [
        (1, 3, 3), (1, 5, 5), (1, 7, 2),
        (3, 2, -4), (5, 4, 6), (4, 5, -3),
        (7, 8, 3), (8, 7, 2), (2, 6, 4),
        (4, 6, 8), (8, 6, 7)
    ]

    # Chuyển về dạng vô hướng: thêm cạnh ngược lại
    edges = []
    for u, v, w in raw_edges:
        edges.append((u - 1, v - 1, w))  # chuyển về chỉ số từ 0
        edges.append((v - 1, u - 1, w))  # thêm cạnh ngược lại

    # Áp dụng thuật toán Kruskal
    mst_cost = kruskals_mst(V, edges)
    print("Tổng trọng số của cây khung nhỏ nhất:", mst_cost)

if __name__ == "__main__":
    main()