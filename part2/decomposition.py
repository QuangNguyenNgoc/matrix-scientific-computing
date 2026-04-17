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

if __name__ == "__main__":
    main()