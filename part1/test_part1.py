from __future__ import annotations

from part1 import (
    back_substitution,
    determinant,
    gaussian_eliminate,
    inverse,
    rank_and_basis,
    verify_solution,
)


def approx_equal_list(a, b, tol=1e-9):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def approx_equal_matrix(A, B, tol=1e-9):
    return len(A) == len(B) and all(approx_equal_list(r1, r2, tol) for r1, r2 in zip(A, B))


def matmul(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    return [
        [sum(A[i][k] * B[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def test_unique_solution():
    A = [[2, 1], [1, 3]]
    b = [5, 6]
    _, info, _ = gaussian_eliminate(A, b)
    assert info["type"] == "unique"
    assert approx_equal_list(info["x"], [1.8, 1.4])


def test_partial_pivoting_needed():
    A = [[0, 2], [1, 3]]
    b = [4, 5]
    _, info, swaps = gaussian_eliminate(A, b)
    assert info["type"] == "unique"
    assert swaps == 1
    assert approx_equal_list(info["x"], [-1.0, 2.0])


def test_near_zero_pivot_solution_and_warning():
    A = [[1e-10, 1.0], [1.0, 1.0]]
    b = [1.0, 2.0]
    _, info, swaps = gaussian_eliminate(A, b)
    assert info["type"] == "unique"
    assert swaps == 1
    assert approx_equal_list(info["x"], [1.0, 1.0], tol=1e-8)
    assert "warnings" not in info


def test_ill_conditioned_system_reports_warning():
    A = [
        [1.0, 1.0],
        [1.0, 1.0 + 1e-10],
    ]
    b = [2.0, 2.0 + 1e-10]
    _, info, _ = gaussian_eliminate(A, b)
    assert info["type"] == "unique"
    assert info["warnings"] == ["pivot is near zero; the system may be ill-conditioned"]
    verification = verify_solution(A, info, b)
    assert verification["residual_norm"] <= 1e-8


def test_infinite_solutions():
    A = [[1, 2, 3], [2, 4, 6]]
    b = [4, 8]
    _, info, _ = gaussian_eliminate(A, b)
    assert info["type"] == "infinite"
    assert info["pivot_columns"] == [0]
    assert info["free_columns"] == [1, 2]
    particular = info["particular"]
    assert approx_equal_list(particular, [4.0, 0.0, 0.0])


def test_near_singular_consistent_system_goes_to_infinite_branch_when_pivot_below_eps():
    A = [[1.0, 1.0], [1.0, 1.0 + 1e-14]]
    b = [2.0, 2.0 + 1e-14]
    _, info, _ = gaussian_eliminate(A, b, eps=1e-12)
    assert info["type"] == "infinite"
    assert info["free_columns"] == [1]


def test_inconsistent_system():
    A = [[1, 1], [1, 1]]
    b = [1, 2]
    _, info, _ = gaussian_eliminate(A, b)
    assert info["type"] == "inconsistent"


def test_near_singular_inconsistent_system_when_rhs_disagrees():
    A = [[1.0, 1.0], [1.0, 1.0 + 1e-14]]
    b = [2.0, 2.0 + 1e-10]
    _, info, _ = gaussian_eliminate(A, b, eps=1e-12)
    assert info["type"] == "inconsistent"


def test_back_substitution():
    U = [[2, 1, -1], [0, 3, 2], [0, 0, 4]]
    c = [8, 7, 12]
    x = back_substitution(U, c)
    assert approx_equal_list(x, [5.333333333333333, 0.3333333333333333, 3.0])


def test_determinant_with_row_swap():
    A = [[0, 1], [1, 0]]
    det = determinant(A)
    assert abs(det + 1.0) <= 1e-9


def test_determinant_singular():
    A = [[1, 2], [2, 4]]
    det = determinant(A)
    assert abs(det) <= 1e-9


def test_determinant_non_square_raises():
    A = [[1, 2, 3], [4, 5, 6]]
    try:
        determinant(A)
        assert False, "Expected ValueError for non-square matrix"
    except ValueError as e:
        assert "square matrix" in str(e)


def test_inverse_2x2():
    A = [[4, 7], [2, 6]]
    A_inv = inverse(A)
    expected = [[0.6, -0.7], [-0.2, 0.4]]
    assert approx_equal_matrix(A_inv, expected)


def test_inverse_identity_check():
    A = [[1, 2, 1], [0, 1, 1], [2, 3, 4]]
    A_inv = inverse(A)
    product = matmul(A, A_inv)
    assert approx_equal_matrix(product, identity(3), tol=1e-8)


def test_inverse_singular_raises():
    A = [[1, 2], [2, 4]]
    try:
        inverse(A)
        assert False, "Expected ValueError for singular matrix"
    except ValueError as e:
        assert "singular" in str(e)


def test_rank_and_basis():
    A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
    info = rank_and_basis(A)
    assert info["rank"] == 2
    assert info["pivot_columns"] == [0, 1]
    assert len(info["column_space_basis"]) == 2
    assert len(info["row_space_basis"]) == 2
    assert len(info["null_space_basis"]) == 1


def test_rank_and_basis_null_space_vector_satisfies_Av_zero():
    A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
    info = rank_and_basis(A)
    basis_vector = info["null_space_basis"][0]
    assert approx_equal_list(matvec(A, basis_vector), [0.0, 0.0, 0.0], tol=1e-9)


def test_verify_solution_unique_branch():
    A = [[3, 2], [1, 2]]
    b = [5, 5]
    _, info, _ = gaussian_eliminate(A, b)
    verification = verify_solution(A, info, b)
    assert verification["is_close"] is True
    assert verification["relative_residual"] <= 1e-9


def test_verify_solution_infinite_branch():
    A = [[1, 2, 3], [2, 4, 6]]
    b = [4, 8]
    _, info, _ = gaussian_eliminate(A, b)
    verification = verify_solution(A, info, b)
    assert verification["is_close"] is True
    assert verification["relative_residual"] <= 1e-9


def test_verify_solution_inconsistent_branch_raises():
    A = [[1, 1], [1, 1]]
    b = [1, 2]
    _, info, _ = gaussian_eliminate(A, b)
    try:
        verify_solution(A, info, b)
        assert False, "Expected ValueError for inconsistent system"
    except ValueError as e:
        assert "inconsistent" in str(e)


if __name__ == "__main__":
    tests = [
        test_unique_solution,
        test_partial_pivoting_needed,
        test_near_zero_pivot_solution_and_warning,
        test_ill_conditioned_system_reports_warning,
        test_infinite_solutions,
        test_near_singular_consistent_system_goes_to_infinite_branch_when_pivot_below_eps,
        test_inconsistent_system,
        test_near_singular_inconsistent_system_when_rhs_disagrees,
        test_back_substitution,
        test_determinant_with_row_swap,
        test_determinant_singular,
        test_determinant_non_square_raises,
        test_inverse_2x2,
        test_inverse_identity_check,
        test_inverse_singular_raises,
        test_rank_and_basis,
        test_rank_and_basis_null_space_vector_satisfies_Av_zero,
        test_verify_solution_unique_branch,
        test_verify_solution_infinite_branch,
        test_verify_solution_inconsistent_branch_raises,
    ]

    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"[PASS] {test.__name__}")

    print(f"\nAll {passed} tests passed.")
