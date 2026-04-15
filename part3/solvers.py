"""
=============================================================================
  Phần 3 — solvers.py
  Giải hệ phương trình tuyến tính Ax = b bằng 3 phương pháp from scratch:
    1) Khử Gauss với Partial Pivoting
    2) Phân rã LU với Partial Pivoting  (PA = LU)
    3) Phương pháp lặp Gauss–Seidel
  
  LƯU Ý THEO YÊU CẦU: Thuật toán được cài đặt bằng LIST THUẦN TÚY 100%.
  NumPy chỉ được phép sử dụng trong việc thiết lập mốc đánh giá kiểm chứng 
  kết quả ở bước verify_solution.
=============================================================================
"""

import numpy as np
import warnings
import math


# ============================================================================
#  HÀM PHỤ TRỢ (Utility helpers)
# ============================================================================

def _forward_substitution(L, b):
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - s) / L[i][i]
    return y


def _backward_substitution(U, c):
    n = len(c)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - s) / U[i][i]
    return x


def _is_strictly_diag_dominant(A):
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= off_diag_sum:
            return False
    return True


def _is_spd(A):
    """
    Kiểm tra ma trận A có đối xứng xác định dương (SPD) hay không bằng list nguyên thuỷ.
    Dùng phân rã Cholesky tự cài đặt để bắt lỗi nếu ma trận không xác định dương.
    """
    n = len(A)
    # Kiểm tra đối xứng
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j] - A[j][i]) > 1e-10:
                return False
    
    # Kiểm tra xác định dương bằng phân rã Cholesky (chỉ tạo nháp để tránh ảnh hưởng)
    L = [[0.0] * n for _ in range(n)]
    try:
        for i in range(n):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    val = A[i][i] - s
                    if val <= 1e-10:  # Không SPD
                        return False
                    L[i][i] = math.sqrt(val)
                else:
                    L[i][j] = (A[i][j] - s) / L[j][j]
        return True
    except Exception:
        return False


# ============================================================================
#  1. PHƯƠNG PHÁP KHỬ GAUSS VỚI PARTIAL PIVOTING
# ============================================================================

def solve_gauss(A, b):
    # Khởi tạo ma trận tăng cường M = [A | b] bằng list thuần
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [float(b[i])] for i in range(n)]

    for k in range(n):
        # Chọn phần tử chốt lớn nhất trên cột k, từ hàng k đến n-1
        max_idx = k
        max_val = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > max_val:
                max_val = abs(M[i][k])
                max_idx = i

        # Hoán vị dòng nếu cần
        if max_idx != k:
            M[k], M[max_idx] = M[max_idx], M[k]

        # Kiểm tra pivot gần 0
        if abs(M[k][k]) < 1e-15:
            raise ValueError(f"Pivot tại cột {k} xấp xỉ 0. Ma trận có thể suy biến.")

        # Khử các dòng phía dưới pivot
        for i in range(k + 1, n):
            factor = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= factor * M[k][j]

    # Thế ngược (Back substitution)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - s) / M[i][i]

    return x


# ============================================================================
#  2. PHÂN RÃ LU VỚI PARTIAL PIVOTING  (PA = LU)
# ============================================================================

def lu_decompose(A):
    n = len(A)
    # Khởi tạo U, L, P bằng nested list thuần túy
    U = [[float(A[i][j]) for j in range(n)] for i in range(n)]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    P = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for k in range(n):
        max_idx = k
        max_val = abs(U[k][k])
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                max_idx = i

        if max_idx != k:
            U[k], U[max_idx] = U[max_idx], U[k]
            P[k], P[max_idx] = P[max_idx], P[k]
            # Hoán vị phần L đã được điền (các cột 0..k-1)
            if k > 0:
                for j in range(k):
                    L[k][j], L[max_idx][j] = L[max_idx][j], L[k][j]

        if abs(U[k][k]) < 1e-15:
            raise ValueError(f"Pivot tại cột {k} xấp xỉ 0 trong phân rã LU.")

        for i in range(k + 1, n):
            factor = U[i][k] / U[k][k]
            L[i][k] = factor
            for j in range(k, n):
                U[i][j] -= factor * U[k][j]

    return P, L, U


def solve_lu(A, b):
    P, L, U = lu_decompose(A)
    n = len(b)

    # Giải Pb = P @ b
    Pb = [0.0] * n
    for i in range(n):
        Pb[i] = sum(P[i][j] * b[j] for j in range(n))

    # Giải Ly = Pb
    y = _forward_substitution(L, Pb)

    # Giải Ux = y
    x = _backward_substitution(U, y)

    return x


# ============================================================================
#  3. PHƯƠNG PHÁP LẶP GAUSS–SEIDEL
# ============================================================================

def solve_gauss_seidel(A, b, tol=1e-8, max_iter=2000):
    n = len(A)
    diag_dominant = _is_strictly_diag_dominant(A)
    spd = _is_spd(A)

    if diag_dominant:
        pass # Tắt print để console benchmark sạch sẽ
    elif spd:
        pass
    else:
        warnings.warn(
            "[Gauss-Seidel] ⚠ Ma trận KHÔNG chéo trội nghiêm ngặt/SPD. "
            "Thuật toán có thể phân kỳ!",
            UserWarning,
            stacklevel=2,
        )

    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            raise ValueError(f"Phần tử đường chéo a[{i},{i}] ≈ 0. Không thể gọi Gauss-Seidel.")

    x = [0.0] * n
    for iteration in range(1, max_iter + 1):
        x_old = x[:]

        for i in range(n):
            sigma_lower = sum(A[i][j] * x[j] for j in range(i))
            sigma_upper = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - sigma_lower - sigma_upper) / A[i][i]

        diff_norm = math.sqrt(sum((x[i] - x_old[i]) ** 2 for i in range(n)))
        if diff_norm < tol:
            return x, iteration

    warnings.warn(
        f"[Gauss-Seidel] Chưa hội tụ sau {max_iter} lặp (||Δx|| = {diff_norm:.2e}).",
        UserWarning,
        stacklevel=2,
    )
    return x, max_iter


# ============================================================================
#  HÀM KIỂM CHỨNG KẾT QUẢ (NumPy CHỈ DÙNG ĐỂ KIỂM CHỨNG NHƯ GIẢNG VIÊN YÊU CẦU)
# ============================================================================

def verify_solution(A, x, b, method_name=""):
    A_np = np.array(A, dtype=float)
    x_np = np.array(x, dtype=float)
    b_np = np.array(b, dtype=float)

    residual = A_np @ x_np - b_np
    rel_error = np.linalg.norm(residual, 2) / np.linalg.norm(b_np, 2)

    x_numpy = np.linalg.solve(A_np, b_np)
    sol_diff = np.linalg.norm(x_np - x_numpy, 2) / (np.linalg.norm(x_numpy, 2) + 1e-30)

    tag = f"[{method_name}] " if method_name else ""
    print(f"{tag}Sai số tương đối ||Ax̂−b||/||b|| = {rel_error:.4e}")
    print(f"{tag}Sai lệch so với chuẩn hệ thống     = {sol_diff:.4e}")
    return rel_error


if __name__ == "__main__":
    print("=" * 60)
    print("  DEMO: Giải hệ phương trình 100% bằng PURE PYTHON LISTS")
    print("=" * 60)

    n = 5
    np.random.seed(42)
    # Tạo ma trận test (Bọc tolist() để thành list)
    A = (np.random.rand(n, n) + n * np.eye(n)).tolist()
    x_true = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = (np.array(A) @ np.array(x_true)).tolist()

    # Đoạn in code cũng xử lý list
    print("\nMa trận A (Dạng Python List của List):")
    for r in A:
        print("  " + " ".join(f"{val:6.2f}" for val in r))
        
    print(f"\nVector b = {[round(val, 4) for val in b]}")
    print(f"Nghiệm thực (chuẩn) = {x_true}")

    print("\n─── 1. Khử Gauss (Partial Pivoting) ───")
    x1 = solve_gauss(A, b)
    print(f"  x = {[round(v, 4) for v in x1]}")
    verify_solution(A, x1, b, "Gauss")

    print("\n─── 2. Phân rã LU ───")
    x2 = solve_lu(A, b)
    print(f"  x = {[round(v, 4) for v in x2]}")
    verify_solution(A, x2, b, "LU")

    print("\n─── 3. Gauss–Seidel (Lặp) ───")
    x3, iters = solve_gauss_seidel(A, b)
    print(f"  x = {[round(v, 4) for v in x3]}  (hội tụ sau {iters} bước)")
    verify_solution(A, x3, b, "Gauss-Seidel")
