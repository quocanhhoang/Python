import networkx as nx
import matplotlib.pyplot as plt

# Hàm kiểm tra liên thông từ danh sách kề
def is_connected_from_adj_list(adj_list):
    if not adj_list:
        return True  # Đồ thị rỗng được xem là liên thông
    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor in adj_list.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

    start_node = next(iter(adj_list))
    dfs(start_node)
    return len(visited) == len(adj_list)

# Danh sách kề của từng hình
adj_list_square = {
    1: [2, 4],
    2: [1, 5],
    4: [1, 5],
    5: [2, 4]
}
adj_list_triangle = {
    3: [6, 7],
    6: [3, 7],
    7: [3, 6]
}
adj_list_line = {
    8: [9],
    9: [8]
}

# Hàm kiểm tra và in kết quả
def check_connectivity(adj_list, name):
    result = is_connected_from_adj_list(adj_list)
    status = "✅ True" if result else "❌ False"
    print(f"{name}: {status}")

# Kiểm tra từng hình
check_connectivity(adj_list_square, "🔷 Hình vuông")
check_connectivity(adj_list_triangle, "🔺 Hình tam giác")
check_connectivity(adj_list_line, "➖ Đoạn thẳng")

