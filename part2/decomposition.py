<<<<<<< feat/manim
import math
import numpy as np
from diagonalization import matrixMultiply, matrixTranspose, findEigen, getColumn

def svdDecomp(matA):
    # Phân rã SVD cho ma trận m x n: A = U * Sigma * V^T
    m = len(matA)
    n = len(matA[0])
    
    for row in matA:
        for val in row:
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Ma trận chứa giá trị NaN hoặc Inf không hợp lệ.")
                
    # Tính tích A^T * A
    matATranspose = matrixTranspose(matA)
    matAtA = matrixMultiply(matATranspose, matA)
    # Tìm giá trị riêng và vector riêng
    evs, matV = findEigen(matAtA)
    # Sắp xếp các giá trị riêng giảm dần kèm theo vector riêng tương ứng
    evPairs = []
    for i in range(n):
        colV = getColumn(matV, i)
        evPairs.append((evs[i], colV))
    evPairs.sort(key=lambda x: x[0], reverse=True)
    
    ortho_V_cols = []
    for i in range(n):
        v = list(evPairs[i][1])
        for u in ortho_V_cols:
            dot_uv = sum(x*y for x, y in zip(v, u))
            v = [x - dot_uv * y for x, y in zip(v, u)]
        norm = math.sqrt(sum(x*x for x in v))
        if norm > 1e-9:
            v = [x/norm for x in v]
        else:
            v = [1.0 if j == i else 0.0 for j in range(n)]
            for u in ortho_V_cols:
                dot_uv = sum(x*y for x, y in zip(v, u))
                v = [x - dot_uv * y for x, y in zip(v, u)]
            norm = math.sqrt(sum(x*x for x in v))
            if norm > 1e-9: v = [x/norm for x in v]
        ortho_V_cols.append(v)
        evPairs[i] = (evPairs[i][0], v)

    singularVals = []
    matVSorted = [[0.0 for col in range(n)] for row in range(n)]
    # Lấy các giá trị kỳ dị bằng căn bậc 2 của các trị riêng dương
    for i in range(n):
        val = evPairs[i][0]
        if val < 1e-9:
            val = 0.0
        singularVals.append(math.sqrt(val))
        for j in range(n):
            matVSorted[j][i] = evPairs[i][1][j]
    # Xây dựng ma trận Sigma kích thước m x n
    matSigma = [[0.0 for col in range(n)] for row in range(m)]
    for i in range(min(m, n)):
        matSigma[i][i] = singularVals[i]
    # Tạo ma trận U cỡ m x m
    colsU = []
    for i in range(min(m, n)):
        if singularVals[i] > 1e-9:
            vecI = [[matVSorted[j][i]] for j in range(n)]
            AVecI = matrixMultiply(matA, vecI)
            uCol = [AVecI[j][0] / singularVals[i] for j in range(m)]
            colsU.append(uCol)
    for i in range(m):
        if len(colsU) == m:
            break
        tempV = [0.0] * m
        tempV[i] = 1.0
        for existU in colsU:
            dotProd = sum([tempV[k] * existU[k] for k in range(m)])
            for k in range(m):
                tempV[k] -= dotProd * existU[k]
        norm = math.sqrt(sum([val**2 for val in tempV]))
        if norm > 1e-9:
            newU = [tempV[k] / norm for k in range(m)]
            colsU.append(newU)
    matU = matrixTranspose(colsU)
    matVTranspose = matrixTranspose(matVSorted)
    return matU, matSigma, matVTranspose

def verifySvd(matA, matU, matSigma, matVT):
    arrA = np.array(matA, dtype=float)
    arrU = np.array(matU, dtype=float)
    arrSigma = np.array(matSigma, dtype=float)
    arrVT = np.array(matVT, dtype=float)
    arrRebuilt = arrU @ arrSigma @ arrVT
    maxError = np.max(np.abs(arrA - arrRebuilt))
    print("* Kiểm chứng SVD")
    print(f"Sai số tái cấu trúc ||A - U*Sigma*V^T||max = {maxError:.2e}")
    if maxError < 1e-4:
        print("Cài đặt SVD đúng (A ~ U*Sigma*V^T).")
    else:
        print("Cài đặt SVD có thể có sai số cao.")
    arrS = np.linalg.svd(arrA)[1]
    # So sánh các giá trị kỳ dị (chỉ lưu min(m, n) phần tử)
    mySingularVals = [matSigma[i][i] for i in range(min(len(matA), len(matA[0])))]
    errSv = np.max(np.abs(np.array(mySingularVals) - arrS))
    print(f"Sai số giá trị kỳ dị so với NumPy = {errSv:.2e}")
    return maxError < 1e-4 and errSv < 1e-4

def demo_svd(matA):
    matU, matSigma, matVT = svdDecomp(matA)
    print("\n* Kết quả phân rã SVD")
    print("Ma trận U (Left Singular Vectors):")
    for row in matU:
        print("  " + " ".join(f"{val:8.4f}" for val in row))
    print("\nMa trận kích thước m x n Sigma (Singular Values):")
    for row in matSigma:
        print("  " + " ".join(f"{val:8.4f}" for val in row))
    print("\nMa trận V^T (Right Singular Vectors Transposed):")
    for row in matVT:
        print("  " + " ".join(f"{val:8.4f}" for val in row))
    verifySvd(matA, matU, matSigma, matVT)

def main():
    try:
        rows = int(input("Nhập số dòng m = "))
        cols = int(input("Nhập số cột n = "))
        print(f"Nhập ma trận {rows}x{cols} (mỗi dòng cách nhau bởi dấu Enter, các phần tử cách nhau bởi khoảng trắng):")
        matA = []
        for i in range(rows):
            row = list(map(float, input().strip().split()))
            if len(row) != cols:
                print(f"Lỗi: Dòng {i+1} không có đủ {cols} phần tử. Vui lòng thử lại.")
                exit()
            matA.append(row)
        demo_svd(matA)
    except ValueError:
        print("Lỗi: Dữ liệu nhập vào chưa hợp lệ.")
=======
from __future__ import annotations

"""
PHÂN RÃ GIÁ TRỊ KỲ DỊ (SVD - Singular Value Decomposition)
Tại sao sử dụng SVD thay vì các loại phân rã khác (LU, QR, Cholesky, Eigen)?

- SVD có thể phân rã MỌI ma trận kích thước m x n bất kỳ (kể cả ma trận chữ nhật hay suy biến).
- Việc tính toán dựa trên ma trận trực giao giúp SVD không bị lỗi nghiêm trọng khi xử lý ma trận gần suy biến.
- SVD không chỉ giải hệ, mà còn cô lập các thành phần quan trọng nhất của ma trận thông qua các giá trị kỳ dị lớn.
"""

import math
from typing import List, Sequence, Tuple, Union

import numpy as np

from diagonalization import (
    Matrix,
    Number,
    Vector,
    _EPS,
    _gram_schmidt,
    _validate_matrix,
    find_eigen,
    get_column,
    mat_mul,
    mat_transpose,
)

# ──────────────────────────────────────────────

def svd_decomp(A: Sequence[Sequence[Number]]) -> Tuple[Matrix, Matrix, Matrix]:
    """
    Phân rã SVD cho ma trận A (m x n): A = U * Sigma * V^T.

    Đầu vào:
    - A: ma trận kích thước m x n (không chứa NaN/Inf)

    Đầu ra:
    - (U, Sigma, V_T): ba ma trận của phân rã SVD
        * U  : ma trận trực giao kích thước m x m
        * Sigma: ma trận đường chéo kích thước m x n (các giá trị kỳ dị giảm dần)
        * V_T: chuyển vị của ma trận trực giao V, kích thước n x n
    """
    mat = _validate_matrix(A)
    m, n = len(mat), len(mat[0])

    At = mat_transpose(mat)
    AtA = mat_mul(At, mat)
    evs, matV = find_eigen(AtA)

    raw_cols = sorted(
        [(evs[i], get_column(matV, i)) for i in range(n)],
        key=lambda p: p[0], reverse=True,
    )
    ortho_V: List[Vector] = _gram_schmidt([list(p[1]) for p in raw_cols])
    while len(ortho_V) < n:
        e = [1.0 if j == len(ortho_V) else 0.0 for j in range(n)]
        ortho_V = _gram_schmidt(ortho_V + [e])

    sigma_vals = [math.sqrt(max(raw_cols[i][0], 0.0)) for i in range(n)]

    V = mat_transpose(ortho_V)

    Sigma: Matrix = [[0.0] * n for _ in range(m)]
    for i in range(min(m, n)):
        Sigma[i][i] = sigma_vals[i]

    cols_U: List[Vector] = []
    for i in range(min(m, n)):
        if sigma_vals[i] > _EPS:
            vi = [[V[j][i]] for j in range(n)]
            Avi = mat_mul(mat, vi)
            cols_U.append([Avi[j][0] / sigma_vals[i] for j in range(m)])

    for i in range(m):
        if len(cols_U) >= m:
            break
        e = [1.0 if j == i else 0.0 for j in range(m)]
        extended = _gram_schmidt(cols_U + [e])
        if len(extended) > len(cols_U):
            cols_U = extended

    U = mat_transpose(cols_U)
    V_T = mat_transpose(V)

    return U, Sigma, V_T

# ──────────────────────────────────────────────

def verify_svd(
    A: Matrix,
    U: Matrix,
    Sigma: Matrix,
    V_T: Matrix,
) -> bool:
    """
    Kiểm chứng kết quả phân rã SVD: tính sai số ||A - U*Sigma*V^T||max và so sánh
    giá trị kỳ dị với NumPy.

    Đầu vào:
    - A: ma trận gốc kích thước m x n
    - U: ma trận trái kích thước m x m
    - Sigma: ma trận đường chéo kích thước m x n
    - V_T: chuyển vị ma trận phải kích thước n x n

    Đầu ra:
    - True nếu cả hai sai số nhỏ hơn 1e-4, ngược lại False
    """
    arrA = np.array(A, dtype=float)
    rebuilt = np.array(U) @ np.array(Sigma) @ np.array(V_T)
    err_recon = float(np.max(np.abs(arrA - rebuilt)))
    print("* Kiểm chứng SVD")
    print(f"Sai số tái cấu trúc ||A - U*Sigma*V^T||max = {err_recon:.2e}")
    print("Cài đặt SVD đúng (A ~ U*Sigma*V^T)." if err_recon < 1e-4
          else "Cài đặt SVD có thể có sai số cao.")

    np_svs = np.linalg.svd(arrA, compute_uv=False)
    my_svs = np.array([Sigma[i][i] for i in range(min(len(A), len(A[0])))])
    err_sv = float(np.max(np.abs(my_svs - np_svs)))
    print(f"Sai số giá trị kỳ dị so với NumPy = {err_sv:.2e}")
    return err_recon < 1e-4 and err_sv < 1e-4

def demo_svd(A: Sequence[Sequence[Number]]) -> None:
    """
    Thực hiện phân rã SVD cho ma trận A và in kết quả ra màn hình.

    Đầu vào:
    - A: ma trận kích thước m x n
    """
    mat = _validate_matrix(A)
    U, Sigma, V_T = svd_decomp(mat)
    print("\n* Kết quả phân rã SVD")
    print("Ma trận U:")
    for row in U:
        print("  " + " ".join(f"{v:8.4f}" for v in row))
    print("\nMa trận Sigma:")
    for row in Sigma:
        print("  " + " ".join(f"{v:8.4f}" for v in row))
    print("\nMa trận V^T:")
    for row in V_T:
        print("  " + " ".join(f"{v:8.4f}" for v in row))
    verify_svd(mat, U, Sigma, V_T)

# ──────────────────────────────────────────────

def main() -> None:
    try:
        rows_n = int(input("Nhập số dòng m = "))
        cols_n = int(input("Nhập số cột n = "))
        print(f"Nhập ma trận {rows_n}x{cols_n} (mỗi dòng cách nhau bởi dấu Enter, "
              "các phần tử cách nhau bởi khoảng trắng):")
        mat: Matrix = []
        for i in range(rows_n):
            row = list(map(float, input().strip().split()))
            if len(row) != cols_n:
                print(f"Lỗi: Dòng {i + 1} không có đủ {cols_n} phần tử.")
                return
            mat.append(row)
        demo_svd(mat)
    except ValueError as e:
        print(f"Lỗi: {e}")
>>>>>>> main

if __name__ == "__main__":
    main()