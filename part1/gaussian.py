from __future__ import annotations

from typing import Dict, List, Sequence, Tuple, Union, Any

Number = Union[int, float]
Matrix = List[List[float]]
Vector = List[float]


def _to_matrix(A: Sequence[Sequence[Number]]) -> Matrix:
    if not A:
        raise ValueError("Matrix A must not be empty.")
    matrix = [list(map(float, row)) for row in A]
    row_length = len(matrix[0])
    if row_length == 0:
        raise ValueError("Matrix A must have at least one column.")
    for row in matrix:
        if len(row) != row_length:
            raise ValueError("Matrix A must be rectangular.")
    return matrix


def _to_vector(b: Sequence[Number]) -> Vector:
    if not b:
        raise ValueError("Vector b must not be empty.")
    return [float(value) for value in b]


def _shape(A: Matrix) -> Tuple[int, int]:
    return len(A), len(A[0])


def _copy_matrix(A: Matrix) -> Matrix:
    return [row[:] for row in A]


def _identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _is_close(value: float, target: float = 0.0, eps: float = 1e-12) -> bool:
    return abs(value - target) <= eps


def _clean_small_entries(A: Matrix, eps: float = 1e-12) -> Matrix:
    for i in range(len(A)):
        for j in range(len(A[0])):
            if abs(A[i][j]) <= eps:
                A[i][j] = 0.0
    return A


def _augment(A: Matrix, b: Vector) -> Matrix:
    if len(A) != len(b):
        raise ValueError("A and b must have the same number of rows.")
    return [A[i][:] + [b[i]] for i in range(len(A))]


def _swap_rows(M: Matrix, i: int, j: int) -> None:
    M[i], M[j] = M[j], M[i]


def _forward_elimination_ref(
    M: Matrix,
    eps: float = 1e-12,
    *,
    pivot_limit: int | None = None,
) -> Tuple[Matrix, int, List[int]]:
    ref = _copy_matrix(M)
    rows, cols = _shape(ref)
    if pivot_limit is None:
        pivot_limit = cols

    pivot_columns: List[int] = []
    swap_count = 0
    pivot_row = 0

    for col in range(min(pivot_limit, cols)):
        if pivot_row >= rows:
            break

        best_row = max(range(pivot_row, rows), key=lambda r: abs(ref[r][col]))
        if abs(ref[best_row][col]) <= eps:
            continue

        if best_row != pivot_row:
            _swap_rows(ref, pivot_row, best_row)
            swap_count += 1

        pivot_columns.append(col)
        pivot_value = ref[pivot_row][col]

        for r in range(pivot_row + 1, rows):
            if abs(ref[r][col]) <= eps:
                ref[r][col] = 0.0
                continue
            factor = ref[r][col] / pivot_value
            for c in range(col, cols):
                ref[r][c] -= factor * ref[pivot_row][c]
            ref[r][col] = 0.0

        pivot_row += 1

    return _clean_small_entries(ref, eps), swap_count, pivot_columns


def _rref(M: Matrix, eps: float = 1e-12) -> Tuple[Matrix, List[int]]:
    rref = _copy_matrix(M)
    rows, cols = _shape(rref)

    pivot_columns: List[int] = []
    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break

        best_row = max(range(pivot_row, rows), key=lambda r: abs(rref[r][col]))
        if abs(rref[best_row][col]) <= eps:
            continue

        if best_row != pivot_row:
            _swap_rows(rref, pivot_row, best_row)

        pivot = rref[pivot_row][col]
        for c in range(col, cols):
            rref[pivot_row][c] /= pivot
        rref[pivot_row][col] = 1.0

        for r in range(rows):
            if r == pivot_row:
                continue
            factor = rref[r][col]
            if abs(factor) <= eps:
                rref[r][col] = 0.0
                continue
            for c in range(col, cols):
                rref[r][c] -= factor * rref[pivot_row][c]
            rref[r][col] = 0.0

        pivot_columns.append(col)
        pivot_row += 1

    return _clean_small_entries(rref, eps), pivot_columns


def _extract_upper_system(ref_augmented: Matrix, n: int) -> Tuple[Matrix, Vector]:
    U = [row[:n] for row in ref_augmented[:n]]
    c = [row[n] for row in ref_augmented[:n]]
    return U, c


def _build_general_solution_from_rref(
    rref_augmented: Matrix,
    variable_count: int,
    pivot_columns: List[int],
    eps: float = 1e-12,
) -> Dict[str, Any]:
    free_columns = [j for j in range(variable_count) if j not in pivot_columns]
    particular = [0.0] * variable_count

    for row_index, pivot_col in enumerate(pivot_columns):
        particular[pivot_col] = rref_augmented[row_index][-1]

    nullspace_basis: List[Vector] = []
    for free_col in free_columns:
        vector = [0.0] * variable_count
        vector[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivot_columns):
            vector[pivot_col] = -rref_augmented[row_index][free_col]
        nullspace_basis.append([0.0 if abs(v) <= eps else v for v in vector])

    parameter_names = [f"t{i + 1}" for i in range(len(free_columns))]
    basis_terms = []
    for name, basis_vector in zip(parameter_names, nullspace_basis):
        basis_terms.append(f"{name}*{basis_vector}")

    if basis_terms:
        general_form = f"x = {particular} + " + " + ".join(basis_terms)
    else:
        general_form = f"x = {particular}"

    return {
        "type": "infinite",
        "particular": particular,
        "nullspace_basis": nullspace_basis,
        "pivot_columns": pivot_columns,
        "free_columns": free_columns,
        "parameters": parameter_names,
        "general_form": general_form,
    }


def back_substitution(U: Sequence[Sequence[Number]], c: Sequence[Number], eps: float = 1e-12) -> Vector:
    upper = _to_matrix(U)
    rhs = _to_vector(c)
    n, m = _shape(upper)
    if n != m:
        raise ValueError("U must be a square matrix.")
    if len(rhs) != n:
        raise ValueError("U and c must have compatible dimensions.")

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(upper[i][i]) <= eps:
            raise ValueError("Back substitution failed because a diagonal pivot is zero.")
        subtotal = sum(upper[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (rhs[i] - subtotal) / upper[i][i]

    return [0.0 if abs(value) <= eps else value for value in x]


def gaussian_eliminate(
    A: Sequence[Sequence[Number]],
    b: Sequence[Number],
    eps: float = 1e-12,
) -> Tuple[Matrix, Dict[str, Any], int]:
    matrix = _to_matrix(A)
    rhs = _to_vector(b)
    rows, cols = _shape(matrix)
    if len(rhs) != rows:
        raise ValueError("A and b must have the same number of rows.")

    augmented = _augment(matrix, rhs)
    ref_augmented, swap_count, pivot_columns = _forward_elimination_ref(
        augmented,
        eps=eps,
        pivot_limit=cols,
    )

    rank_A = len(pivot_columns)

    for row in ref_augmented:
        if all(abs(row[j]) <= eps for j in range(cols)) and abs(row[-1]) > eps:
            return ref_augmented, {
                "type": "inconsistent",
                "pivot_columns": pivot_columns,
                "message": "The system is inconsistent, so it has no solution.",
            }, swap_count

    if cols == rows and rank_A == cols:
        U, c_vector = _extract_upper_system(ref_augmented, cols)
        x = back_substitution(U, c_vector, eps=eps)
        return ref_augmented, {
            "type": "unique",
            "x": x,
            "pivot_columns": pivot_columns,
        }, swap_count

    rref_augmented, rref_pivot_columns = _rref(augmented, eps=eps)
    solution_info = _build_general_solution_from_rref(
        rref_augmented,
        cols,
        [col for col in rref_pivot_columns if col < cols],
        eps=eps,
    )
    solution_info["rref_augmented"] = rref_augmented
    return ref_augmented, solution_info, swap_count


def determinant(A: Sequence[Sequence[Number]], eps: float = 1e-12) -> float:
    matrix = _to_matrix(A)
    rows, cols = _shape(matrix)
    if rows != cols:
        raise ValueError("determinant(A) requires a square matrix.")

    ref_matrix, swap_count, _ = _forward_elimination_ref(matrix, eps=eps, pivot_limit=cols)
    det = (-1.0 if swap_count % 2 else 1.0)
    for i in range(rows):
        det *= ref_matrix[i][i]

    return 0.0 if abs(det) <= eps else det


def inverse(A: Sequence[Sequence[Number]], eps: float = 1e-12) -> Matrix:
    matrix = _to_matrix(A)
    n, m = _shape(matrix)
    if n != m:
        raise ValueError("inverse(A) requires a square matrix.")

    augmented = [matrix[i] + _identity(n)[i] for i in range(n)]

    pivot_row = 0
    for col in range(n):
        best_row = max(range(pivot_row, n), key=lambda r: abs(augmented[r][col]))
        if abs(augmented[best_row][col]) <= eps:
            raise ValueError("Matrix is singular, so it does not have an inverse.")

        if best_row != pivot_row:
            _swap_rows(augmented, pivot_row, best_row)

        pivot = augmented[pivot_row][col]
        for j in range(2 * n):
            augmented[pivot_row][j] /= pivot
        augmented[pivot_row][col] = 1.0

        for r in range(n):
            if r == pivot_row:
                continue
            factor = augmented[r][col]
            if abs(factor) <= eps:
                augmented[r][col] = 0.0
                continue
            for j in range(2 * n):
                augmented[r][j] -= factor * augmented[pivot_row][j]
            augmented[r][col] = 0.0

        pivot_row += 1

    inverse_matrix = [row[n:] for row in _clean_small_entries(augmented, eps)]
    return inverse_matrix


def rank_and_basis(A: Sequence[Sequence[Number]], eps: float = 1e-12) -> Dict[str, Any]:
    matrix = _to_matrix(A)
    rows, cols = _shape(matrix)
    rref_matrix, pivot_columns = _rref(matrix, eps=eps)
    rank = len(pivot_columns)
    free_columns = [j for j in range(cols) if j not in pivot_columns]

    column_space_basis = []
    for pivot_col in pivot_columns:
        column_space_basis.append([matrix[i][pivot_col] for i in range(rows)])

    row_space_basis = []
    for row in rref_matrix:
        if any(abs(value) > eps for value in row):
            row_space_basis.append(row[:])

    null_space_basis: List[Vector] = []
    for free_col in free_columns:
        vector = [0.0] * cols
        vector[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivot_columns):
            vector[pivot_col] = -rref_matrix[row_index][free_col]
        null_space_basis.append([0.0 if abs(v) <= eps else v for v in vector])

    return {
        "rank": rank,
        "pivot_columns": pivot_columns,
        "free_columns": free_columns,
        "rref": rref_matrix,
        "column_space_basis": column_space_basis,
        "row_space_basis": row_space_basis,
        "null_space_basis": null_space_basis,
    }


def verify_solution(
    A: Sequence[Sequence[Number]],
    x: Union[Sequence[Number], Dict[str, Any]],
    b: Sequence[Number],
    tol: float = 1e-9,
) -> Dict[str, Any]:
    import numpy as np

    matrix = np.array(A, dtype=float)
    rhs = np.array(b, dtype=float)

    if isinstance(x, dict):
        if x.get("type") == "unique":
            candidate = np.array(x["x"], dtype=float)
        elif x.get("type") == "infinite":
            candidate = np.array(x["particular"], dtype=float)
        else:
            raise ValueError("Cannot verify an inconsistent system because no solution vector exists.")
    else:
        candidate = np.array(x, dtype=float)

    residual = matrix @ candidate - rhs
    residual_norm = float(np.linalg.norm(residual))
    rhs_norm = float(np.linalg.norm(rhs))
    relative_residual = residual_norm / rhs_norm if rhs_norm > 0 else residual_norm

    return {
        "is_close": bool(np.allclose(matrix @ candidate, rhs, atol=tol, rtol=tol)),
        "residual_norm": residual_norm,
        "relative_residual": relative_residual,
        "numpy_solution": np.linalg.lstsq(matrix, rhs, rcond=None)[0].tolist(),
    }


__all__ = [
    "gaussian_eliminate",
    "back_substitution",
    "determinant",
    "inverse",
    "rank_and_basis",
    "verify_solution",
]
