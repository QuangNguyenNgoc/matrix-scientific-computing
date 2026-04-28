# Đồ án: Ma trận và Tính toán Khoa học

## Giới thiệu

Đồ án 1 - môn học Toán Ứng Dụng và Thống kê. Nội dung các tệp kèm theo gồm mã, các tệp khác như `report.pdf` chứa báo cáo chính cho đồ án.

### Nội dung chính

- **Phần 1: Phép khử Gauss và ứng dụng** - Nghiên cứu phép khử Gauss và chiến lược chọn phần tử chốt (Partial Pivoting). Ứng dụng để giải hệ phương trình tuyến tính, tính định thức, và tìm ma trận nghịch đảo.

- **Phần 2: Phân rã ma trận và trực quan hóa với Manim** - Chéo hóa và phân rã kỳ dị (SVD). Sử dụng Manim để trực quan hóa.

- **Phần 3: Giải hệ phương trình và phân tích hiệu năng** - So sánh các giải thuật trực tiếp (Gauss, LU) với phương pháp lặp (Gauss-Seidel) qua các bài đo đạc (benchmark). Phân tích mối quan hệ giữa số điều kiện (Condition Number) và độ tin cậy của nghiệm số.

## Cấu trúc dự án

```
Group_12/
├── part1/              # Thuật toán khử Gauss và ứng dụng
├── part2/              # Chéo hóa và phân rã ma trận SVD
├── part3/              # Giải hệ phương trình và Benchmark
├── notebooks/          # Demo Jupyter Notebook và phân tích dữ liệu
├── tests/              # Hệ thống kiểm thử tự động
├── docs/               # Tài liệu hướng dẫn
├── report/             # Mã nguồn Typst cho báo cáo
├── requirements.txt    # Các gói phụ thuộc cơ bản
└── requirements-manim.txt  # Các gói cho Manim (Linux)
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

- [Thành viên 1 - GitHub Link](https://github.com/username)
- [Thành viên 2 - GitHub Link](https://github.com/username)
- [Thành viên 3 - GitHub Link](https://github.com/username)

## Tài liệu bổ sung

- [Hướng dẫn cài đặt môi trường](docs/02%20-%20Environment%20Setup.md)
- [Hướng dẫn đóng góp](docs/03%20-%20CONTRIBUTING.md)
- [Tóm tắt yêu cầu](docs/Tóm%20tắt%20cơ%20bản%20yêu%20cầu.md)
