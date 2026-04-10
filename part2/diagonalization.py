import math
import numpy as np
import cmath

def getColumn(matrix, colIndex):
    return [row[colIndex] for row in matrix]

def matrixMultiply(matA, matB):
    rowsA = len(matA)
    colsA = len(matA[0])
    colsB = len(matB[0])
    result = [[0.0 for col in range(colsB)] for row in range(rowsA)]
    for i in range(rowsA):
        for j in range(colsB):
            sumProd = 0.0
            for k in range(colsA):
                sumProd += matA[i][k] * matB[k][j]
            result[i][j] = sumProd
    return result

def matrixTranspose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0.0 for row in range(rows)] for col in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

def gaussInverse(matrix):
    n = len(matrix)
    augMat = [row[:] + [1.0 if i == j else 0.0 for step in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = augMat[i][i]
        if abs(pivot) < 1e-9:
            for k in range(i + 1, n):
                if abs(augMat[k][i]) > abs(pivot):
                    augMat[i], augMat[k] = augMat[k], augMat[i]
                    pivot = augMat[i][i]
                    break
        for j in range(2 * n):
            augMat[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = augMat[k][i]
                for j in range(2 * n):
                    augMat[k][j] -= factor * augMat[i][j]
    return [row[n:] for row in augMat]

def charPoly(matrix):
    # Trả về mảng hệ số đa thức đặc trưng [cn, c(n-1), ..., c0]
    n = len(matrix)
    c = [1.0]
    matB = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        if k == 1:
            matM = matrix
        else:
            matM = matrixMultiply(matrix, matB)
        traceM = sum(matM[i][i] for i in range(n))
        ak = - traceM / k
        c.append(ak)
        matB = [[matM[i][j] + (ak if i == j else 0.0) for j in range(n)] for i in range(n)]
    return c

def findRoots(coeffs):
    # Tìm các rễ phương trình đa thức đặc trưng
    n = len(coeffs) - 1
    roots = [cmath.rect(1.5, 2 * math.pi * k / n) for k in range(n)]
    for step in range(150):
        for k in range(n):
            polyVal = 0.0
            for j in range(n + 1):
                polyVal += coeffs[j] * (roots[k] ** (n - j))
            den = 1.0
            for j in range(n):
                if j != k:
                    den *= (roots[k] - roots[j])
            if abs(den) > 1e-15:
                roots[k] -= polyVal / den
    return [float(x.real) for x in roots if abs(x.imag) < 1e-3]

def gaussBasis(matrix, ev):
    # Cài đặt thuật toán khử Gauss trên (A - lambda * I)x = 0 để lấy không gian nghiệm
    n = len(matrix)
    matM = [[matrix[i][j] - (ev if i == j else 0.0) for j in range(n)] for i in range(n)]
    pivotCols = []
    lead = 0
    aug = [row[:] for row in matM]
    for r in range(n):
        if lead >= n:
            break
        maxVal = 0.0
        maxIdx = r
        for i in range(r, n):
            if abs(aug[i][lead]) > maxVal:
                maxVal = abs(aug[i][lead])
                maxIdx = i
        if maxVal < 1e-6:
            lead += 1
            continue
        aug[maxIdx], aug[r] = aug[r], aug[maxIdx]
        pivotCols.append(lead)
        lv = aug[r][lead]
        for j in range(n):
            aug[r][j] /= lv
        for i in range(n):
            if i != r:
                lv = aug[i][lead]
                for j in range(n):
                    aug[i][j] -= lv * aug[r][j]
        lead += 1
    freeCols = [j for j in range(n) if j not in pivotCols]
    if not freeCols:
        if pivotCols:
            pivotCols.pop()
        freeCols.append(n - 1)
    basis = []
    for f in freeCols:
        v = [0.0] * n
        v[f] = 1.0
        for rIdx, pCol in enumerate(pivotCols):
            if rIdx < n:
                v[pCol] = -aug[rIdx][f]
        norm = math.sqrt(sum(x*x for x in v))
        if norm > 1e-9:
            v = [x/norm for x in v]
        basis.append(v)
    return basis

def findEigen(matrix):
    # Detect bậc
    n = len(matrix)
    if n <= 4:
        # Bậc <= 4: Dùng khử Gauss
        coeffs = charPoly(matrix)
        evs = findRoots(coeffs)
        evs.sort(reverse=True)
        uniqueEvs = []
        for ev in evs:
            if not any(abs(ev - u) < 1e-4 for u in uniqueEvs):
                uniqueEvs.append(ev)  
        finalEvs = []
        pRows = []
        for ev in uniqueEvs:
            basis = gaussBasis(matrix, ev)
            for vec in basis:
                finalEvs.append(ev)
                pRows.append(vec)
        # Phân phối và giới hạn lại số chiều vector tương ứng bậc N
        sortedPairs = sorted(zip(finalEvs, pRows), key=lambda x: x[0], reverse=True)
        sortedEvs = [p[0] for p in sortedPairs][:n]
        sortedVecs = [p[1] for p in sortedPairs][:n]
        # Bổ sung vector fallback cho tình trạng zero pivot array loss
        while len(sortedEvs) < n:
            sortedEvs.append(0.0)
            extraV = [0.0] * n
            extraV[len(sortedEvs) - 1] = 1.0
            sortedVecs.append(extraV)
        return sortedEvs, matrixTranspose(sortedVecs)
    else:
        # Bậc > 4: Dùng thư viện numpy.linalg.eig
        arrM = np.array(matrix, dtype=float)
        npEvs, npEvecs = np.linalg.eig(arrM)
        npEvs = npEvs.real
        npEvecs = npEvecs.real
        # Sắp xếp giảm dần để đồng nhất
        idx = np.argsort(npEvs)[::-1]
        npEvs = npEvs[idx]
        npEvecs = npEvecs[:, idx]
        return npEvs.tolist(), npEvecs.tolist()

def diagonalize(matrix):
    # Chéo hóa ma trận thành A = P * D * P^-1
    n = len(matrix)
    evs, matP = findEigen(matrix)
    matD = [[0.0 for col in range(n)] for row in range(n)]
    for i in range(n):
        matD[i][i] = evs[i]  
    matPInv = gaussInverse(matP)
    return matP, matD, matPInv

def verify(matrixA, matP, matD, matPInv):
    # Sử dụng Numpy để đổi trọng số sai số
    arrA = np.array(matrixA, dtype=float)
    arrP = np.array(matP, dtype=float)
    arrD = np.array(matD, dtype=float)
    arrPInv = np.array(matPInv, dtype=float)
    arrRebuilt = arrP @ arrD @ arrPInv
    maxError = np.max(np.abs(arrA - arrRebuilt))
    print("* Kiểm chứng chéo hóa")
    print(f"Sai số tái cấu trúc ||A - P*D*P^-1||max = {maxError:.2e}")
    if maxError < 1e-4:
        print("Cài đặt chéo hóa đúng (A ~ P D P^-1).")
    else:
        print("Cài đặt chéo hóa có thể có sai số cao.")   
    arrEvs = np.linalg.eig(arrA)[0]
    myEvs = np.diag(arrD)
    errEv = np.max(np.abs(np.sort(myEvs)[::-1] - np.sort(arrEvs.real)[::-1]))
    print(f"Sai số giá trị riêng so với NumPy = {errEv:.2e}")
    return maxError < 1e-4 and errEv < 1e-4

def main():
    try:
        size = int(input("Nhập kích thước ma trận vuông n = "))
        print(f"Nhập ma trận {size}x{size} (mỗi dòng cách nhau bởi dấu Enter, các phần tử cách nhau bởi khoảng trắng):")
        matA = []
        for i in range(size):
            row = list(map(float, input().strip().split()))
            if len(row) != size:
                print(f"Lỗi: Dòng {i+1} không có đủ {size} phần tử. Vui lòng thử lại.")
                exit()
            matA.append(row)
        matP, matD, matPInv = diagonalize(matA)
        print("\n* Kết quả chéo hóa")
        print("Ma trận đổi cơ sở P (Các vector riêng nằm trên các cột):")
        for row in matP:
            print("  " + " ".join(f"{val:8.4f}" for val in row))
        print("\nMa trận đường chéo D (Các giá trị riêng):")
        for row in matD:
            print("  " + " ".join(f"{val:8.4f}" for val in row))
        print("\nMa trận P^-1:")
        for row in matPInv:
            print("  " + " ".join(f"{val:8.4f}" for val in row))
        verify(matA, matP, matD, matPInv)
    except ValueError:
        print("Lỗi: Dữ liệu nhập vào chưa hợp lệ.")

if __name__ == "__main__":
    main()
