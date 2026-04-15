"""
=============================================================================
  Phần 3 — benchmark.py
  Chạy thực nghiệm đo hiệu năng và phân tích tính ổn định số học.
  
  Hai nhóm thực nghiệm:
    A) Đo thời gian thực thi & sai số tương đối cho n ∈ {50,100,200,500,1000}
    B) Phân tích ổn định: ma trận Hilbert (ill-conditioned) vs SPD (well-cond.)

  Kết quả được lưu vào file CSV trong thư mục part3/results/
=============================================================================
"""

import os
import sys
import time
import warnings
import numpy as np
import csv

# Thêm đường dẫn để import solvers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solvers import solve_gauss, solve_lu, solve_gauss_seidel


# ============================================================================
#  CẤU HÌNH
# ============================================================================

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Kích thước ma trận cho thực nghiệm A
SIZES_TIMING = [50, 100, 200, 500, 1000]

# Số lần lặp lấy trung bình
NUM_RUNS = 5

# Kích thước ma trận Hilbert cho thực nghiệm B
SIZES_HILBERT = [3, 5, 8, 10, 12, 15]

# Kích thước ma trận SPD cho thực nghiệm B
SIZES_SPD_STABILITY = [5, 10, 20, 50, 100]


# ============================================================================
#  HÀM SINH MA TRẬN
# ============================================================================

def generate_diag_dominant_matrix(n, seed=None):
    """
    Sinh ma trận chéo trội nghiêm ngặt nxn.
    A = random(n,n) + n * I  →  đảm bảo |a_ii| > Σ_{j≠i} |a_ij|.
    """
    if seed is not None:
        np.random.seed(seed)
    A = np.random.rand(n, n) + n * np.eye(n)
    return A


def generate_hilbert_matrix(n):
    """
    Sinh ma trận Hilbert H_n có phần tử H_{ij} = 1 / (i + j - 1).
    Ma trận Hilbert có số điều kiện cực lớn (ill-conditioned).
    """
    H = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            H[i, j] = 1.0 / (i + j + 1)    # index 0-based nên (i+1)+(j+1)-1 = i+j+1
    return H


def generate_spd_matrix(n, seed=None):
    """
    Sinh ma trận đối xứng xác định dương (SPD) ngẫu nhiên nxn.
    A = M @ M^T + I  →  đảm bảo SPD.
    """
    if seed is not None:
        np.random.seed(seed)
    M = np.random.rand(n, n)
    A = M @ M.T + np.eye(n)
    return A


def relative_error(A, x_hat, b):
    """Tính sai số tương đối: ||Ax̂ - b||₂ / ||b||₂"""
    residual = A @ x_hat - b
    return np.linalg.norm(residual, 2) / np.linalg.norm(b, 2)


def solution_error(x_hat, x_true):
    """Tính sai số nghiệm: ||x̂ - x_true||₂ / ||x_true||₂"""
    return np.linalg.norm(x_hat - x_true, 2) / (np.linalg.norm(x_true, 2) + 1e-30)


# ============================================================================
#  THỰC NGHIỆM A — Đo thời gian & sai số theo kích thước n
# ============================================================================

def run_timing_benchmark():
    """
    Đo thời gian thực thi trung bình (5 lần chạy) và sai số tương đối
    cho mỗi phương pháp với n ∈ {50, 100, 200, 500, 1000}.
    """
    print("=" * 70)
    print("  THỰC NGHIỆM A: Đo thời gian thực thi & sai số tương đối")
    print("=" * 70)

    results = []

    for n in SIZES_TIMING:
        print(f"\n{'─' * 50}")
        print(f"  n = {n}")
        print(f"{'─' * 50}")

        # Sinh ma trận chéo trội (đảm bảo Gauss-Seidel hội tụ)
        A = generate_diag_dominant_matrix(n, seed=42)
        x_true = np.ones(n)             # nghiệm thực = vector toàn 1
        b = A @ x_true

        methods = {
            "Gauss": lambda A_, b_: solve_gauss(A_.tolist(), b_.tolist()),
            "LU": lambda A_, b_: solve_lu(A_.tolist(), b_.tolist()),
        }

        # Gauss-Seidel cần xử lý riêng vì trả thêm iterations
        for name, solver in methods.items():
            times = []
            for run in range(NUM_RUNS):
                t_start = time.perf_counter()
                x_hat = solver(A, b)
                t_end = time.perf_counter()
                times.append(t_end - t_start)

            avg_time = np.mean(times)
            rel_err = relative_error(A, x_hat, b)
            sol_err = solution_error(x_hat, x_true)

            print(f"  {name:15s} | t_avg = {avg_time:.6f}s | "
                  f"res_err = {rel_err:.4e} | sol_err = {sol_err:.4e}")

            results.append({
                "n": n,
                "method": name,
                "avg_time": avg_time,
                "relative_error": rel_err,
                "solution_error": sol_err,
            })

        # Gauss-Seidel
        # Tắt print bên trong solve_gauss_seidel khi benchmark
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            times_gs = []
            iters_total = 0
            for run in range(NUM_RUNS):
                t_start = time.perf_counter()
                x_hat_gs, iters = solve_gauss_seidel(A.tolist(), b.tolist())
                t_end = time.perf_counter()
                times_gs.append(t_end - t_start)
                iters_total += iters

            avg_time_gs = np.mean(times_gs)
            rel_err_gs = relative_error(A, x_hat_gs, b)
            sol_err_gs = solution_error(x_hat_gs, x_true)
            avg_iters = iters_total / NUM_RUNS

            print(f"  {'Gauss-Seidel':15s} | t_avg = {avg_time_gs:.6f}s | "
                  f"res_err = {rel_err_gs:.4e} | sol_err = {sol_err_gs:.4e} | "
                  f"avg_iters = {avg_iters:.0f}")

            results.append({
                "n": n,
                "method": "Gauss-Seidel",
                "avg_time": avg_time_gs,
                "relative_error": rel_err_gs,
                "solution_error": sol_err_gs,
            })

    # Lưu kết quả ra CSV
    csv_path = os.path.join(RESULTS_DIR, "timing_benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "method", "avg_time",
                                               "relative_error", "solution_error"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Kết quả đã lưu tại: {csv_path}")
    return results


# ============================================================================
#  THỰC NGHIỆM B — Phân tích ổn định số (Stability Analysis)
# ============================================================================

def run_stability_benchmark():
    """
    So sánh tính ổn định số khi giải hệ với:
      - Ma trận Hilbert (ill-conditioned, κ rất lớn)
      - Ma trận SPD ngẫu nhiên (well-conditioned, κ nhỏ)
    """
    print("\n" + "=" * 70)
    print("  THỰC NGHIỆM B: Phân tích Ổn định Số (Stability Analysis)")
    print("=" * 70)

    results = []

    # --- B1. Ma trận Hilbert (ill-conditioned) ---
    print("\n▶ B1. Ma trận Hilbert (Ill-conditioned)")
    print(f"{'─' * 60}")
    print(f"  {'n':>4s} | {'κ(H_n)':>15s} | {'Gauss err':>12s} | "
          f"{'LU err':>12s} | {'G-S err':>12s}")
    print(f"{'─' * 60}")

    for n in SIZES_HILBERT:
        H = generate_hilbert_matrix(n)
        x_true = np.ones(n)
        b = H @ x_true
        cond_num = np.linalg.cond(H, p=2)

        row = {"n": n, "matrix_type": "Hilbert", "condition_number": cond_num}

        # Gauss
        try:
            x_g = solve_gauss(H.tolist(), b.tolist())
            err_g = solution_error(x_g, x_true)
        except Exception:
            err_g = float("inf")
        row["error_Gauss"] = err_g

        # LU
        try:
            x_lu = solve_lu(H.tolist(), b.tolist())
            err_lu = solution_error(x_lu, x_true)
        except Exception:
            err_lu = float("inf")
        row["error_LU"] = err_lu

        # Gauss-Seidel
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                x_gs, iters = solve_gauss_seidel(H.tolist(), b.tolist(),
                                                  tol=1e-10, max_iter=5000)
            err_gs = solution_error(x_gs, x_true)
        except Exception:
            err_gs = float("inf")
        row["error_GaussSeidel"] = err_gs

        results.append(row)
        print(f"  {n:4d} | {cond_num:15.4e} | {err_g:12.4e} | "
              f"{err_lu:12.4e} | {err_gs:12.4e}")

    # --- B2. Ma trận SPD ngẫu nhiên (well-conditioned) ---
    print(f"\n▶ B2. Ma trận SPD ngẫu nhiên (Well-conditioned)")
    print(f"{'─' * 60}")
    print(f"  {'n':>4s} | {'κ(A)':>15s} | {'Gauss err':>12s} | "
          f"{'LU err':>12s} | {'G-S err':>12s}")
    print(f"{'─' * 60}")

    for n in SIZES_SPD_STABILITY:
        A_spd = generate_spd_matrix(n, seed=123)
        x_true = np.ones(n)
        b = A_spd @ x_true
        cond_num = np.linalg.cond(A_spd, p=2)

        row = {"n": n, "matrix_type": "SPD_Random", "condition_number": cond_num}

        # Gauss
        try:
            x_g = solve_gauss(A_spd.tolist(), b.tolist())
            err_g = solution_error(x_g, x_true)
        except Exception:
            err_g = float("inf")
        row["error_Gauss"] = err_g

        # LU
        try:
            x_lu = solve_lu(A_spd.tolist(), b.tolist())
            err_lu = solution_error(x_lu, x_true)
        except Exception:
            err_lu = float("inf")
        row["error_LU"] = err_lu

        # Gauss-Seidel
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                x_gs, iters = solve_gauss_seidel(A_spd.tolist(), b.tolist(),
                                                  tol=1e-10, max_iter=5000)
            err_gs = solution_error(x_gs, x_true)
        except Exception:
            err_gs = float("inf")
        row["error_GaussSeidel"] = err_gs

        results.append(row)
        print(f"  {n:4d} | {cond_num:15.4e} | {err_g:12.4e} | "
              f"{err_lu:12.4e} | {err_gs:12.4e}")

    # Lưu kết quả ra CSV
    csv_path = os.path.join(RESULTS_DIR, "stability_benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "n", "matrix_type", "condition_number",
            "error_Gauss", "error_LU", "error_GaussSeidel"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n Kết quả đã lưu tại: {csv_path}")
    return results


# ============================================================================
#  MAIN — Chạy toàn bộ thực nghiệm
# ============================================================================

if __name__ == "__main__":
    print("PHẦN 3 — BENCHMARK: Giải Hệ PT & Phân Tích Hiệu Năng")

    timing_results = run_timing_benchmark()
    stability_results = run_stability_benchmark()

    print("\n" + "=" * 70)
    print("  ĐÃ HOÀN THÀNH TẤT CẢ THỰC NGHIỆM!")
    print(f"  Kết quả lưu tại thư mục: {RESULTS_DIR}")
    print("=" * 70)
