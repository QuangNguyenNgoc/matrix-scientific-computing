# Part 1 - Gaussian Elimination and Basic Matrix Operations

## 1. Mục tiêu

Phần 1 của đồ án tập trung cài đặt các phép toán cơ bản trong đại số tuyến tính số bằng Python, không dùng thư viện đại số tuyến tính để thực hiện trực tiếp thuật toán chính. Nội dung chính gồm:

- Giải hệ phương trình tuyến tính bằng phép khử Gauss
- Thế ngược cho hệ tam giác trên
- Tính định thức của ma trận vuông
- Tính ma trận nghịch đảo bằng Gauss-Jordan
- Tính hạng ma trận và các cơ sở liên quan
- Kiểm chứng nghiệm bằng NumPy
- Viết test để kiểm tra các trường hợp cơ bản

---

## 2. Cấu trúc thư mục

```text
part1/
├── __init__.py
├── gaussian.py
├── determinant.py
├── inverse.py
├── rank_basis.py
├── utils.py
├── verify.py
├── test_part1.py
├── part1_demo.ipynb
└── README_part1.md
```

---

## 3. Chức năng từng file

### `__init__.py`
Export các hàm chính để có thể import trực tiếp từ package `part1`, gồm:

- `gaussian_eliminate`
- `back_substitution`
- `determinant`
- `inverse`
- `rank_and_basis`
- `verify_solution`

### `gaussian.py`
Chứa phần cài đặt chính cho phép khử Gauss và các bước liên quan:

- `back_substitution(U, c, eps=...)`: giải hệ tam giác trên `Ux = c`
- `_forward_elimination_ref(...)`: đưa ma trận về dạng bậc thang dòng (REF)
- `_rref(...)`: đưa ma trận về dạng bậc thang dòng rút gọn (RREF)
- `_build_general_solution_from_rref(...)`: dựng nghiệm tổng quát khi hệ có vô số nghiệm
- `_extract_upper_system(...)`: tách ma trận tăng cường dạng REF thành `U` và `c`
- `gaussian_eliminate(A, b, eps=...)`: hàm chính giải hệ `Ax = b`

### `determinant.py`
Tính định thức của ma trận vuông bằng phép khử Gauss. Giá trị định thức được lấy từ tích các phần tử đường chéo sau khi khử, có xét đến số lần đổi dòng.

### `inverse.py`
Tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan trên ma trận ghép `[A | I]`.

### `rank_basis.py`
Tính:

- hạng của ma trận
- cơ sở của không gian cột
- cơ sở của không gian dòng
- cơ sở của không gian nghiệm

### `utils.py`
Chứa các hàm phụ trợ và kiểu dữ liệu dùng chung:

- `Number`
- `Matrix`
- `Vector`
- `_to_matrix`
- `_to_vector`
- `_shape`
- `_copy_matrix`
- `_identity`
- `_clean_small_entries`
- `_augment`
- `_swap_rows`

### `verify.py`
Kiểm chứng nghiệm bằng NumPy, tính residual norm, relative residual và nghiệm xấp xỉ từ `numpy.linalg.lstsq`.

### `test_part1.py`
Chứa các test cho Part 1. File hiện tại gồm 11 test case cơ bản.

### `part1_demo.ipynb`
Notebook minh họa cách sử dụng các hàm trong Part 1.

---

## 4. Cách chạy

### 4.1. Chạy test
Từ thư mục gốc của project:

```powershell
python -m pytest part1/test_part1.py
```

### 4.2. Chạy notebook demo
1. Mở file `part1/part1_demo.ipynb`
2. Bấm `Run All`

---

## 5. Bộ test hiện có

File `test_part1.py` hiện kiểm tra các trường hợp sau:

1. Hệ có nghiệm duy nhất
2. Trường hợp cần đổi dòng do pivot đầu tiên bằng 0
3. Hệ có vô số nghiệm
4. Hệ vô nghiệm
5. Hàm thế ngược
6. Định thức khi có đổi dòng
7. Định thức của ma trận suy biến
8. Nghịch đảo của ma trận `2x2`
9. Kiểm tra `A * A^{-1} = I`
10. Tính rank và các basis
11. Kiểm chứng nghiệm bằng NumPy

---