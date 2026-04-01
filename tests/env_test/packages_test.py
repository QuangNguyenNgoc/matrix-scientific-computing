# check_env.py


def check_python():
    import sys

    print(f"[OK] Python version: {sys.version}")


def check_numpy():
    import numpy as np

    a = np.array([[1, 2], [3, 4]])
    print("[OK] NumPy working:", a.shape)


def check_scipy():
    import scipy

    print("[OK] SciPy version:", scipy.__version__)


def check_sympy():
    import sympy as sp

    x = sp.symbols("x")
    expr = sp.expand((x + 1) ** 2)
    print("[OK] SymPy working:", expr)


def check_matplotlib():
    import matplotlib.pyplot as plt

    print("[OK] Matplotlib imported")


def check_ipykernel():
    import ipykernel

    print("[OK] ipykernel version:", ipykernel.__version__)


def main():
    print("=== Checking core environment ===")
    check_python()
    check_numpy()
    check_scipy()
    check_sympy()
    check_matplotlib()
    check_ipykernel()
    print("=== DONE ===")


if __name__ == "__main__":
    main()

# # EXPECT OUTPUT:

# === Checking core environment ===
# [OK] Python version: 3.11.x ...
# [OK] NumPy working: (2, 2)
# [OK] SciPy version: 1.11.4
# [OK] SymPy working: x**2 + 2*x + 1
# [OK] Matplotlib imported
# [OK] ipykernel version: ...
# === DONE ===
