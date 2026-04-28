# Phần 2: Chéo hóa & Phân rã Ma trận SVD

Xây dựng các hàm để **Chéo hóa ma trận** và **Phân rã giá trị kỳ dị (SVD)**. Sử dụng `numpy` ở phân hệ đánh giá, kiểm chứng sai số.

## Link video demo Manim
https://youtu.be/sWpLmDTU0R0

## 1. Cấu trúc thư mục

```text
part2/
│
├── diagonalization.py
├── decomposition.py
├── test.ipynb
└── readme.md
```

## 2. Chi tiết Thuật toán áp dụng

### A. Chéo Hóa Ma Trận (`diagonalization.py`)
Mục tiêu bài toán là biểu diễn ma trận vuông $A$ thành $A = P \cdot D \cdot P^{-1}$.
Các kỹ thuật tích hợp:
- Tính đa thức đặc trưng: Nhận hệ số $c_n, c_{n-1}, ...$ ổn định từ ma trận $A$ bằng thuật toán Faddeev-LeVerrier.
- Tìm trị riêng: Triển khai phương pháp lặp song song Durand-Kerner trên không gian số phức để tìm nghiệm đa thức.
- Tìm vector riêng: Tái sử dụng thuật toán Khử Gauss-Jordan của *phần 1 (`part1.rank_basis`)*. Từ đó tìm ra các cơ sở cho dòng suy biến.
- Trực chuẩn hoá (Gram-Schmidt): Đảm bảo các vector riêng độc lập tuyến tính và ở dạng trực chuẩn (orthonormal).
- Fallback: Áp dụng các thuật toán gốc rễ trên cho ma trận có kích thước $n \le 4$. Kích thước lớn hơn sẽ được fallback nhường vị trí cho thư viện tính toán lớn để đảm bảo tốc độ. Báo `ValueError` chống lỗi nghiêm trọng đối với các ma trận khuyết.

### B. Phân rã SVD (`decomposition.py`)
SVD là ma trận giải quyết bài toán biểu diễn: $A = U \cdot \Sigma \cdot V^T$.
Đặc tính vượt trội:
- Hỗ trợ mọi ma trận: Kể cả trường hợp $M \times N$ hình chữ nhật, ma trận hạng hụt (rank-deficient).
- Logic trích xuất:
  1. Xây dựng $A^T \cdot A$ (luôn đối xứng).
  2. Tái sử dụng module chéo hóa phía trên để nới giá trị riêng và vector riêng $\rightarrow$ trực tiếp suy ra ma trận đường chéo $\Sigma$ và ma trận $V$.
  3. Hoàn thiện $U$ bằng $A \cdot v_i / \sigma_i$.
  4. Bổ khuyết không gian null của $U$ (nếu thiếu dòng) bằng **Trực chuẩn hóa Gram-Schmidt** để duy trì tính chất $U^T \cdot U = I$.

---

## 3. Hướng dẫn kiểm thử

Mã nguồn được thiết kế với giao diện cho phép nhập liệu ma trận trực tiếp từ terminal.

### 3.1. Chạy demo qua terminal
Kiểm duyệt song song theo thời gian thực với NumPy. Sai số tái cấu trúc yêu cầu ở ngưỡng $< 10^{-4}$.

*Chạy tính toán Chéo hóa:*
```python
python part2/diagonalization.py
```

*Chạy tính toán SVD:*
```python
python part2/decomposition.py
```

### 3.2. Test bằng notebook (`test.ipynb`)
Bao gồm 10 Test Cases (5 cho Chéo hoá, 5 cho SVD):
- Trị riêng phân biệt, trị riêng lặp.
- Ma trận chữ nhật dư dòng, dư cột.
- Ma trận suy biến, khuyết hệ số, chứa NaN/Inf.

Nhấn **Run All** trong Jupyter hoặc VS Code để chạy.

## 4. Kiểm thử với Manim

## Lưu ý liên quan đến dependencies
- Phần core gồm `decomposition.py` và `diagonalization.py` sử dụng các thư viện được liệt kê trong `requirements.txt` (file chính).
- Mặt khác, video Manim (`manim_scene.py`) sử dụng `requirements-manim.txt` và sử dụng **Linux** làm môi trường chính (do nhiều thư viện chỉ hỗ trợ cho hệ điều hành này).
- Phương án cài đặt tốt nhất cho manim(cho Linux):
```bash
# Tạo môi trường
python -m venv venv-manim
source venv-manim/bin/activate

# Cài thư viện Python
pip install -r part2/requirements-manim.txt

# Cài các dependencies hỗ trợ
sudo apt install build-essential python3-dev pkg-config \ libcairo2-dev libpango1.0-dev ffmpeg dvisvgm
