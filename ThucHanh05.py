#Phương pháp K-map
from typing import List, Set, Tuple, Dict
from itertools import product

# =========================
# Karnaugh Map (2..4 vars)
# =========================

def gray_code(n: int) -> List[str]:
    """Danh sách mã Gray n bit theo thứ tự chuẩn."""
    if n == 0:
        return [""]
    prev = gray_code(n - 1)
    return ["0" + x for x in prev] + ["1" + x for x in reversed(prev)]

def bits_of(n: int, k: int) -> str:
    return format(n, f"0{k}b")

def pow2s_up_to(n: int) -> List[int]:
    x, out = 1, []
    while x <= n:
        out.append(x)
        x <<= 1
    return out

class KMap:
    """
    K-map cho 2..4 biến.
    mode='SOP': điền 1 tại minterms, nhóm 1 để tạo SOP
    mode='POS': điền 0 tại maxterms, nhóm 0 để tạo POS
    """
    def __init__(self, num_vars: int, mode: str = "SOP",
                 minterms: List[int] = None, maxterms: List[int] = None,
                 var_names: List[str] = None):
        assert num_vars in (2, 3, 4), "Hỗ trợ 2–4 biến."
        self.n = num_vars
        self.mode = mode.upper()
        assert self.mode in ("SOP", "POS")
        self.var_names = var_names or [chr(ord('A') + i) for i in range(self.n)]

        self.size = 1 << self.n
        self.minterms = sorted(set(minterms or []))
        self.maxterms = sorted(set(maxterms or []))

        # Bố cục hàng/cột theo Gray:
        # 2 biến: hàng=biến 0, cột=biến 1
        # 3 biến: hàng=biến 0, cột=biến 1..2 (2 bit)
        # 4 biến: hàng=biến 0..1 (2 bit), cột=biến 2..3 (2 bit)
        if self.n == 2:
            self.row_bits, self.col_bits = 1, 1
        elif self.n == 3:
            self.row_bits, self.col_bits = 1, 2
        else:  # n == 4
            self.row_bits, self.col_bits = 2, 2

        self.row_labels = gray_code(self.row_bits)
        self.col_labels = gray_code(self.col_bits)

        # Lập ánh xạ minterm -> (row, col) theo thứ tự biến [A,B,C,D]
        self.index_map: Dict[int, Tuple[int, int]] = {}
        self._build_index_map()

        # Khởi tạo lưới giá trị
        self.grid = [[0 for _ in self.col_labels] for _ in self.row_labels]
        self._fill_grid()

    def _build_index_map(self):
        # Với nhãn hàng & cột (mã Gray), khớp bit theo thứ tự biến
        # n=2: row=A, col=B
        # n=3: row=A, col=BC
        # n=4: row=AB, col=CD
        for r, rb in enumerate(self.row_labels):
            for c, cb in enumerate(self.col_labels):
                if self.n == 2:
                    full = rb + cb               # A | B
                elif self.n == 3:
                    full = rb + cb               # A | B C
                else:  # 4
                    full = rb + cb               # A B | C D
                m = int(full, 2)
                self.index_map[m] = (r, c)

    def _fill_grid(self):
        if self.mode == "SOP":
            ones = set(self.minterms)
            for m in range(self.size):
                r, c = self.index_map[m]
                self.grid[r][c] = 1 if m in ones else 0
        else:  # POS
            zeros = set(self.maxterms)
            for m in range(self.size):
                r, c = self.index_map[m]
                self.grid[r][c] = 0 if m in zeros else 1

    # ---------- Tìm nhóm hình chữ nhật có quấn biên ----------
    def _rect_cells(self, r0: int, c0: int, h: int, w: int) -> Set[Tuple[int, int]]:
        R, C = len(self.row_labels), len(self.col_labels)
        cells = set()
        for dr in range(h):
            for dc in range(w):
                cells.add(((r0 + dr) % R, (c0 + dc) % C))
        return cells

    def _all_groups(self, target: int) -> List[Set[Tuple[int, int]]]:
        """Tạo tất cả nhóm hình chữ nhật giá trị = target (1 cho SOP, 0 cho POS)."""
        R, C = len(self.row_labels), len(self.col_labels)
        total = R * C
        sizes = list(reversed(pow2s_up_to(total)))  # duyệt nhóm lớn trước không bắt buộc
        groups = set()
        for s in sizes:
            # s = h*w, với h,w là lũy thừa 2 và h<=R, w<=C
            factors = [(h, s // h) for h in pow2s_up_to(s) if s % h == 0]
            # chỉ lấy các cặp (h,w) hợp lệ trong lưới
            hw_list = [(h, w) for (h, w) in factors if h <= R and w <= C]
            for h, w in hw_list:
                for r0 in range(R):
                    for c0 in range(C):
                        cells = self._rect_cells(r0, c0, h, w)
                        if all(self.grid[r][c] == target for (r, c) in cells):
                            groups.add(frozenset(cells))
        # Loại nhóm bị chứa hoàn toàn trong nhóm lớn hơn (giữ "prime groups")
        groups = list(groups)
        prime = []
        for g in groups:
            if not any((g < h) for h in groups):  # g là tập con thực sự của h?
                prime.append(set(g))
        # Sắp xếp giảm dần theo kích thước nhóm
        prime.sort(key=lambda s: (-len(s), sorted(list(s))))
        return prime

    # ---------- Chuyển nhóm -> hạng thức ----------
    def _cells_to_minterms(self, cells: Set[Tuple[int, int]]) -> List[int]:
        rev_index = {v: k for k, v in self.index_map.items()}
        return [rev_index[(r, c)] for (r, c) in cells]

    def _group_to_term_SOP(self, cells: Set[Tuple[int, int]]) -> str:
        """Từ nhóm 1s suy ra tích (product term) cho SOP."""
        ms = self._cells_to_minterms(cells)
        k = self.n
        # Tìm bit cố định trên tất cả minterm
        bit_cols = list(zip(*(bits_of(m, k) for m in ms)))  # list of tuples cột bit
        parts = []
        for i, col in enumerate(bit_cols):
            if all(b == '0' for b in col):
                parts.append(f"{self.var_names[i]}'")
            elif all(b == '1' for b in col):
                parts.append(f"{self.var_names[i]}")
        return "".join(parts) if parts else "1"

    def _group_to_term_POS(self, cells: Set[Tuple[int, int]]) -> str:
        """Từ nhóm 0s suy ra tổng (sum term) cho POS."""
        ms = self._cells_to_minterms(cells)
        k = self.n
        bit_cols = list(zip(*(bits_of(m, k) for m in ms)))
        # Tổng (OR) gồm biến “không đổi” nhưng nghịch dấu so với SOP:
        # - nếu bit luôn 0  -> (A + ...) chứa A (không đảo)
        # - nếu bit luôn 1  -> chứa A' trong dấu cộng
        # Biểu diễn chuẩn POS: (x + y + z)
        lits = []
        for i, col in enumerate(bit_cols):
            if all(b == '0' for b in col):
                lits.append(f"{self.var_names[i]}")
            elif all(b == '1' for b in col):
                lits.append(f"{self.var_names[i]}'")
        return "(" + " + ".join(lits) + ")" if lits else "(1)"

    # ---------- Chọn nhóm để phủ (ưu tiên lớn, thiết yếu, rồi tham lam) ----------
    def _select_groups(self, groups: List[Set[Tuple[int, int]]], target: int) -> List[Set[Tuple[int, int]]]:
        """Chọn tập nhóm phủ toàn bộ ô = target."""
        R, C = len(self.row_labels), len(self.col_labels)
        universe = {(r, c) for r in range(R) for c in range(C) if self.grid[r][c] == target}
        selected: List[Set[Tuple[int, int]]] = []

        if not universe:
            return []

        # 1) Nhóm thiết yếu: ô chỉ nằm trong đúng 1 nhóm
        cover_count: Dict[Tuple[int, int], int] = {cell: 0 for cell in universe}
        for g in groups:
            for cell in (g & universe):
                cover_count[cell] += 1

        essential = []
        for cell, cnt in cover_count.items():
            if cnt == 1:
                # tìm nhóm duy nhất chứa cell
                for g in groups:
                    if cell in g:
                        essential.append(g)
                        break
        # thêm thiết yếu
        for g in essential:
            if g not in selected:
                selected.append(g)

        covered = set().union(*selected) if selected else set()
        covered &= universe

        # 2) Tham lam: thêm nhóm phủ nhiều ô chưa phủ nhất
        remaining = universe - covered
        pool = [g for g in groups if g not in selected]
        while remaining:
            best, gain = None, -1
            for g in pool:
                g_gain = len(g & remaining)
                if g_gain > gain:
                    best, gain = g, g_gain
            if not best or gain <= 0:
                break
            selected.append(best)
            covered |= (best & universe)
            remaining = universe - covered
            pool.remove(best)

        return selected

    # ---------- Giao diện chính ----------
    def simplify(self):
        if self.mode == "SOP":
            target = 1
            all_groups = self._all_groups(target=1)
            chosen = self._select_groups(all_groups, target=1)
            terms = [self._group_to_term_SOP(g) for g in chosen]
            expr = " + ".join(sorted(set(terms), key=terms.index)) if terms else "0"
            return expr, chosen, all_groups
        else:  # POS
            target = 0
            all_groups = self._all_groups(target=0)
            chosen = self._select_groups(all_groups, target=0)
            terms = [self._group_to_term_POS(g) for g in chosen]
            expr = "".join(sorted(set(terms), key=terms.index)) if terms else "(1)"
            return expr, chosen, all_groups

    def pretty_grid(self) -> str:
        """In lưới K-map với nhãn Gray cho trực quan."""
        header = [" " * (self.row_bits + 2)] + self.col_labels
        lines = ["\t".join(header)]
        for r, rb in enumerate(self.row_labels):
            row = [rb + " |"] + [str(self.grid[r][c]) for c in range(len(self.col_labels))]
            lines.append("\t".join(row))
        return "\n".join(lines)

# =========================
# Ví dụ sử dụng
# =========================
if __name__ == "__main__":
    # --- Ví dụ SOP:
    # km = KMap(num_vars=4, mode="SOP", minterms=[5,10,11,12,13,14,15])
    # expr, chosen_groups, all_groups = km.simplify()
    # print("K-map (SOP) grid:")
    # print(km.pretty_grid())
    # print("\nNhóm (đã chọn): kích thước và các ô (r,c):")
    # for g in chosen_groups:
    #     print(f"  size={len(g)} -> {sorted(list(g))}")
    # print("\nBiểu thức rút gọn (SOP):")
    # print("  f =", expr)

    # # --- Ví dụ POS:
    # km2 = KMap(num_vars=4, mode="POS", maxterms=[0,1,2,3,4,6,7,8,9])
    # expr2, chosen_groups2, _ = km2.simplify()
    # print("\nK-map (POS) grid:")
    # print(km2.pretty_grid())
    # print("\nBiểu thức rút gọn (POS):")
    # print("  F =", expr2)
    print("================================")
    print("1. Chọn chế độ SOP")
    print("2. Chọn chế độ POS")
    print("================================")
    choice = input("Lựa chọn (1 hoặc 2): ").strip()
    if choice == '1':
        mode = "SOP"
        raw = input("Nhập danh sách minterm (cách nhau bằng dấu phẩy): ")
        minterms = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]
        num_vars = max(2, (max(minterms).bit_length() if minterms else 2))
        km = KMap(num_vars=num_vars, mode=mode, minterms=minterms)
        expr, chosen_groups, all_groups = km.simplify()
        print("\nK-map (SOP) grid:")
        print(km.pretty_grid())
        print("\nNhóm (đã chọn): kích thước và các ô (r,c):")
        for g in chosen_groups:
            print(f"  size={len(g)} -> {sorted(list(g))}")
        print("\nBiểu thức rút gọn (SOP):")
        print("  f =", expr)
    elif choice == '2':
        mode = "POS"
        raw = input("Nhập danh sách maxterm (cách nhau bằng dấu phẩy): ")
        maxterms = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]
        num_vars = max(2, (max(maxterms).bit_length() if maxterms else 2))
        km = KMap(num_vars=num_vars, mode=mode, maxterms=maxterms)
        expr, chosen_groups, all_groups = km.simplify()
        print("\nK-map (POS) grid:")
        print(km.pretty_grid())
        print("\nNhóm (đã chọn): kích thước và các ô (r,c):")
        for g in chosen_groups:
            print(f"  size={len(g)} -> {sorted(list(g))}")
        print("\nBiểu thức rút gọn (POS):")
        print("  F =", expr)
    else:
        print("Lựa chọn không hợp lệ.")