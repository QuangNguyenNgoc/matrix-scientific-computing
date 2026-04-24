from __future__ import annotations
from collections.abc import Sequence
from numbers import Number
from typing import Any, Dict, Union

import numpy as np

"""
Kiểm chứng nghiệm bằng NumPy.
"""

def verify_solution(
    A: Sequence[Sequence[Number]],
    x: Union[Sequence[Number], Dict[str, Any]],
    b: Sequence[Number],
    tol: float = 1e-9,
) -> Dict[str, Any]:
    """
    Đầu vào:
    - A: ma trận hệ số
    - x_or_info: vector nghiệm hoặc solution_info từ gaussian_eliminate
    - b: vector vế phải
    - tol: ngưỡng so sánh gần đúng

    Đầu ra:
    - dict chứa:
      - is_close
      - residual_norm
      - relative_residual
      - numpy_solution
    """
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