## 1. Mục tiêu

Tài liệu này quy định cách làm việc nhóm để:

- tránh conflict
- tránh sửa chéo file
- dễ review
- dễ tích hợp code trước deadline

---

## 2. Branching Strategy

### Các nhánh chính

- `main`: nhánh ổn định, gần với bản nộp
- `feature/*`: nhánh làm task

### Quy tắc

- Không commit trực tiếp lên `main`
- Mỗi task làm trên **1 branch riêng**

Ví dụ:

```text
feature/gauss-forward
feature/partial-pivoting
feature/determinant
feature/inverse
feature/rank-basis
feature/lu-decomposition
feature/diagonalization
feature/manim-demo
feature/benchmark
```

## 3. Quy tắc sửa file

### Được phép

- sửa file thuộc task của mình
- thêm test cho task của mình
- sửa lỗi nhỏ nếu có liên quan trực tiếp tới task

### Không nên tự ý

- đổi cấu trúc project
- đổi tên file đang dùng chung
- sửa code task người khác
- sửa API public mà không báo nhóm

## 4. Quy tắc API / interface

Các hàm core phải giữ đúng interface đã thống nhất.
Ví dụ:

```python
def determinant(A, *, eps=1e-10) -> float:
    ...
```

Nếu cần đổi API:

- báo nhóm trước
- giải thích lý do
- chỉ đổi sau khi thống nhất

## 5. Coding style

### Yêu cầu chung

- code rõ ràng, dễ đọc
- ưu tiên clean code
- có docstring ngắn cho hàm chính
- dùng type hint nếu có thể

```python
def back_substitution(U: list[list[float]], c: list[float], *, eps: float = 1e-10) -> list[float]:
    """Solve upper triangular system Ux = c."""
```

## 7. Quy tắc với thư viện

### Được phép

- dùng `numpy`, `scipy`, `sympy` để verify
- dùng `matplotlib` cho plotting
- dùng `manim` cho visualization

### Không được dùng để implement thuật toán

- `numpy.linalg.solve`
- `numpy.linalg.inv`
- `scipy.linalg.*`
- `sympy` solver / `rref` / `echelon_form`

## 8. Test và Definition of Done

Một task được coi là hoàn thành khi:

- code chạy được
- đúng API đã thống nhất
- có test hoặc demo case
- không phá code hiện có
- có mô tả ngắn trong Pull Request

Với hàm chính:

- nên có ít nhất 5 test cases
- có edge cases nếu phù hợp

## 9. Pull Request template

Mỗi PR nên có nội dung ngắn như sau:

### Title

```text
[Part1] Implement determinant
```

### Nội dung

- Mục tiêu task
- File đã sửa
- API liên quan
- Đã test gì
- Còn điểm gì cần reviewer chú ý

## 10. Quy tắc trao đổi

- Có bug / blocker thì báo sớm
- Không để task "im lặng" quá lâu
- Nếu phải sửa chéo task người khác, cần báo trước
- Khi hoàn thành task, nhắn nhóm để review / merge

## 12. Kết luận

Mỗi người chịu trách nhiệm rõ phần của mình, làm việc trên branch riêng, giữ interface ổn định, và ưu tiên merge nhỏ – sớm – an toàn.

---

# 3. Checklist trước khi nộp

```md
# SUBMISSION_CHECKLIST.md

## 1. Cấu trúc thư mục

- [ ] Có `README.md`
- [ ] Có `requirements.txt`
- [ ] Có `requirements-manim.txt`
- [ ] Có thư mục `part1/`
- [ ] Có thư mục `part2/`
- [ ] Có thư mục `part3/`
- [ ] Có `report/report.pdf`

---

## 2. Part 1

- [ ] Có `gaussian.py`
- [ ] Có `determinant.py`
- [ ] Có `inverse.py`
- [ ] Có `rank_basis.py`
- [ ] Có `part1_demo.ipynb`
- [ ] Có partial pivoting
- [ ] Có verify bằng NumPy
- [ ] Mỗi hàm chính có test/demo case
- [ ] Không dùng `numpy.linalg.solve` / `inv` để implement

---

## 3. Part 2

- [ ] Có `decomposition.py`
- [ ] Có `diagonalization.py`
- [ ] Có `manim_demo.py` hoặc `manim_scene.py`
- [ ] Có `demo_video.mp4`
- [ ] Video render được, độ phân giải ổn
- [ ] Video dài ít nhất 2 phút
- [ ] Core Part 2 không phụ thuộc Manim
- [ ] Có verify decomposition/diagonalization bằng NumPy nếu cần

---

## 4. Part 3

- [ ] Có `solvers.py` hoặc file tương đương
- [ ] Có `benchmark.py`
- [ ] Có `analysis.ipynb`
- [ ] Có ít nhất 3 phương pháp giải
- [ ] Có Gauss từ Part 1
- [ ] Có decomposition method từ Part 2
- [ ] Có ít nhất 1 iterative method
- [ ] Có benchmark với nhiều kích thước ma trận
- [ ] Có biểu đồ log-log
- [ ] Có phân tích Hilbert vs SPD/random matrix

---

## 5. Report

- [ ] Có trang bìa
- [ ] Có mục lục
- [ ] Có Part 1
- [ ] Có Part 2
- [ ] Có Part 3
- [ ] Có kết luận
- [ ] Có tài liệu tham khảo
- [ ] Có phân công công việc từng thành viên

---

## 6. README

- [ ] Có hướng dẫn cài Python
- [ ] Có hướng dẫn tạo `venv`
- [ ] Có hướng dẫn cài `requirements.txt`
- [ ] Có hướng dẫn riêng cho Manim
- [ ] Có ghi rõ thư viện chỉ dùng để verify
- [ ] Có mô tả cách chạy code chính

---

## 7. Kiểm tra kỹ thuật cuối

- [ ] Clone repo ở máy khác vẫn đọc được cấu trúc
- [ ] `requirements.txt` cài được
- [ ] Notebook mở được
- [ ] Video mở được
- [ ] Không còn file rác / file tạm
- [ ] Không push `venv/`
- [ ] Không push file lớn không cần thiết
- [ ] Không thiếu file đầu ra quan trọng

---

## 8. Kiểm tra học thuật

- [ ] Mọi thành viên hiểu phần mình làm
- [ ] Không copy code không kiểm soát
- [ ] Nếu có dùng AI, cả nhóm vẫn giải thích được code
- [ ] Có thể trình bày khi bị hỏi vấn đáp

---

## 9. Trước khi nộp

- [ ] Merge code cuối cùng vào nhánh ổn định
- [ ] Review nhanh toàn bộ repo
- [ ] Mở thử `report.pdf`
- [ ] Mở thử `demo_video.mp4`
- [ ] Mở thử các notebook
- [ ] Đảm bảo đúng tên file/thư mục cần nộp
```
