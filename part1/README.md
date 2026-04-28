# Part 1 - Gaussian Elimination and Basic Matrix Operations

## 1. Mục tiêu

Phần 1 của đồ án cài đặt các phép toán đại số tuyến tính cơ bản bằng Python. Phần này gồm phép khử Gauss, thế ngược, định thức, nghịch đảo, hạng ma trận, các basis liên quan và kiểm chứng kết quả bằng NumPy.

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

## 3. Chức năng từng file

### `__init__.py`
File này export các hàm chính để có thể import trực tiếp từ package `part1`, gồm `gaussian_eliminate`, `back_substitution`, `determinant`, `inverse`, `rank_and_basis` và `verify_solution`.

### `gaussian.py`
File này cài đặt phép khử Gauss với partial pivoting, hàm thế ngược cho hệ tam giác trên, hàm đưa ma trận về dạng RREF để phân loại nghiệm, hàm dựng nghiệm tổng quát khi hệ có vô số nghiệm, và cảnh báo khi pivot quá nhỏ. Nếu trong quá trình khử xuất hiện pivot gần 0, `solution_info` sẽ kèm warning `"pivot is near zero; the system may be ill-conditioned"`.

### `determinant.py`
File này tính định thức của ma trận vuông bằng phép khử Gauss.

### `inverse.py`
File này tính ma trận nghịch đảo bằng Gauss-Jordan. Nếu ma trận suy biến hoặc không vuông thì hàm sẽ báo lỗi thay vì trả kết quả sai.

### `rank_basis.py`
File này trả về hạng của ma trận.

### `utils.py`
File này chứa các kiểu dữ liệu và các hàm phụ trợ như chuẩn hóa đầu vào, lấy kích thước ma trận, tạo ma trận đơn vị, ghép ma trận với vector vế phải, đổi dòng và dọn các giá trị rất nhỏ về 0.

### `verify.py`
File này dùng NumPy để kiểm chứng một nghiệm đã tìm được.

### `test_part1.py`
File này chứa bộ test cho Part 1. Bộ test dùng để kiểm tra các trường hợp cơ bản và kiểm tra thêm các tình huống gần suy biến, ill-conditioned, các trường hợp lỗi và việc basis của null space thỏa `Av = 0`.

### `part1_demo.ipynb`
Minh họa cách dùng các hàm trong Part 1. Notebook cho phép quan sát kết quả sau khi chạy, gồm case near-zero pivot, case vô số nghiệm, case vô nghiệm và case ill-conditioned.

## 4. Cách chạy

### 4.1. Chạy test
Từ thư mục gốc của project, chạy:

```powershell
python -m pytest part1/test_part1.py
```

### 4.2. Chạy notebook demo
Mở file `part1/part1_demo.ipynb`, sau đó chọn `Run All` để xem toàn bộ các case minh họa.

## 5. Bộ test hiện có

File `test_part1.py` hiện kiểm tra các nhóm trường hợp sau:

1. Hệ có nghiệm duy nhất.
2. Trường hợp cần đổi dòng do pivot đầu tiên bằng 0.
3. Trường hợp near-zero pivot.
4. Trường hợp ill-conditioned.
5. Hệ có vô số nghiệm.
6. Hệ gần suy biến, với pivot nhỏ hơn `eps`, được coi là vô số nghiệm.
7. Hệ vô nghiệm.
8. Hệ gần suy biến nhưng vế phải lệch đủ lớn để được coi là vô nghiệm.
9. Hàm thế ngược.
10. Định thức khi có đổi dòng.
11. Định thức của ma trận suy biến.
12. Định thức với ma trận không vuông.
13. Nghịch đảo của ma trận `2x2`.
14. Kiểm tra `A * A^{-1} = I`.
15. Ma trận suy biến khi gọi `inverse()`.
16. Tính rank và các basis.
17. Kiểm tra trực tiếp một vector trong `null_space_basis` thỏa `Av = 0`.
18. `verify_solution()` ở nhánh nghiệm duy nhất.
19. `verify_solution()` ở nhánh vô số nghiệm.
20. `verify_solution()` ở nhánh vô nghiệm.

## 6. Ghi chú về tính toán số

Phần cài đặt này dùng một ngưỡng `eps` để nhận diện các giá trị gần 0. Vì vậy, với những ma trận gần suy biến hoặc ill-conditioned, kết quả phân loại có thể phụ thuộc vào `eps`. File test và notebook đều có thêm các case near-zero pivot và ill-conditioned để minh họa giới hạn số học của phương pháp.
