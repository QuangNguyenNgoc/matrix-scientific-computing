# Phần 1 - Phép khử Gauss và các ứng dụng

## Các tệp đi kèm
- `gaussian.py`: cài đặt đầy đủ toàn bộ yêu cầu của Phần 1.
- `determinant.py`: tệp bao ngoài cho hàm `determinant`.
- `inverse.py`: tệp bao ngoài cho hàm `inverse`.
- `rank_basis.py`: tệp bao ngoài cho hàm `rank_and_basis`.
- `test_part1.py`: bộ kiểm thử thủ công cho Phần 1.

## Các hàm công khai
- `gaussian_eliminate(A, b)`
- `back_substitution(U, c)`
- `determinant(A)`
- `inverse(A)`
- `rank_and_basis(A)`
- `verify_solution(A, x, b)`

## Ghi chú
- Phần cài đặt thuật toán **không** sử dụng NumPy / SciPy / SymPy.
- NumPy chỉ xuất hiện trong hàm `verify_solution`.
- Hàm `gaussian_eliminate` xử lý 3 trường hợp:
  1. hệ có nghiệm duy nhất,
  2. hệ có vô số nghiệm,
  3. hệ vô nghiệm.