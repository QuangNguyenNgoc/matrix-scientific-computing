# Đồ án: Ma trận và Tính toán Khoa học

## Giới thiệu

Đồ án 1 - môn học Toán Ứng Dụng và Thống kê. Nội dung các tệp kèm theo gồm mã, các tệp khác như `report.pdf` chứa báo cáo chính cho đồ án.

### Nội dung chính

- **Phần 1: Phép khử Gauss và ứng dụng** - Nghiên cứu phép khử Gauss và chiến lược chọn phần tử chốt (Partial Pivoting). Ứng dụng để giải hệ phương trình tuyến tính, tính định thức, và tìm ma trận nghịch đảo.

- **Phần 2: Phân rã ma trận và trực quan hóa với Manim** - Chéo hóa và phân rã kỳ dị (SVD). Sử dụng Manim để trực quan hóa.

- **Phần 3: Giải hệ phương trình và phân tích hiệu năng** - So sánh các giải thuật trực tiếp (Gauss, LU) với phương pháp lặp (Gauss-Seidel) qua các bài đo đạc (benchmark). Phân tích mối quan hệ giữa số điều kiện (Condition Number) và độ tin cậy của nghiệm số.

- **Report** - Được viết bằng Typst Rust, ghi chép thông tin báo cáo trong file `report.typ` và được xuất thành file `report.pdf` để dễ dàng theo dõi.

## Cấu trúc dự án

```
Group_12/
├── part1/                          # Phép khử Gauss và ứng dụng
│   ├── gaussian.py                 # Thuật toán Gauss với Partial Pivoting
│   ├── determinant.py              # Tính định thức
│   ├── inverse.py                  # Tính ma trận nghịch đảo
│   ├── rank_basis.py               # Tính hạng và cơ sở
│   ├── utils.py                    # Hàm tiện ích
│   ├── test_part1.py               # Kiểm thử
│   ├── part1_demo.ipynb            # Demo Jupyter
│   └── README.md
├── part2/                          # Phân rã ma trận và Manim
│   ├── decomposition.py            # Phân rã Cholesky, QR, LU
│   ├── diagonalization.py          # Chéo hóa và SVD
│   ├── manim_scene.py              # Animation Manim
│   ├── test.ipynb                  # Demo Jupyter
│   ├── requirements-manim.txt      # Gói Manim (Linux)
│   └── README.md
├── part3/                          # Giải hệ phương trình và Benchmark
│   ├── solvers.py                  # Giải pháp (Gauss, LU, Gauss-Seidel)
│   ├── benchmark.py                # Đo hiệu năng
│   ├── analysis.ipynb              # Phân tích kết quả
│   ├── results/                    # Kết quả benchmark
├── report/                         # Báo cáo (Typst)
│   ├── report.typ                  # Main file code của báo cáo
│   ├── report.pdf                  # File báo cáo theo dõi chính
│   ├── chapters/
├── requirements.txt                # Gói cơ bản
└── README.md
```

## Cài đặt

### Yêu cầu

- **Python 3.11** hoặc cao hơn

### Hướng dẫn cài đặt

#### 1. Tạo môi trường (Virtual Environment)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

#### 2. Cài đặt

**Dành cho việc chạy các file core logic (.py, ipynb)**

```bash
pip install -r requirements.txt
```

Các gói sẽ được cài đặt:

- `numpy==1.26.4` - Thư viện tính toán số
- `scipy==1.11.4` - Các hàm tính toán khoa học nâng cao
- `sympy==1.12` - Tính toán hình thức (symbolic computation)
- `matplotlib==3.8.4` - Vẽ biểu đồ
- `ipykernel==6.29.5` - Kernel cho Jupyter Notebook
- `pandas==2.2.2` - Xử lý dữ liệu

#### Lưu ý về môi trường Manim

Nhóm đã cài đặt Manim trên **Linux (WSL)** như một phương án làm việc phụ để đảm bảo tính ổn định khi render video. Để có thể kiểm thử [Xem chi tiết tại đây](part2/readme.md#4-kiểm-thử-với-manim).

## Thành viên nhóm

- Nguyễn Ngọc Quang - 24120127
- Đinh Đức Hiếu - 24120002
- Liên Trung Hiếu - 24120049
- Trương Đình Nhật Huy - 24120064
- Đặng Quang Tiến - 24120149
