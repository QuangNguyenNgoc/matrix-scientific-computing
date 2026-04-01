# General Requirements

- Python 3.11.x (khuyến nghị: 3.11.9)
- pip (đi kèm Python)

## 1. Cài đặt Python

### 2.1 Nếu máy chưa có Python

Tải và cài Python 3.11 từ trang chính thức:

- https://www.python.org/downloads/

**Khuyến nghị:** dùng Python **3.11.9**

### 2.2 Nếu máy có nhiều phiên bản Python

Kiểm tra các phiên bản đang có:

```bash
python --version
py --version
py -0
```

## 2. Setup (Windows – dùng cho toàn bộ project)

Áp dụng cho:

- Part 1 (Gaussian, determinant, inverse, rank)
- Part 2 (core logic: decomposition, diagonalization)
- Part 3 (benchmark, analysis, notebook)

```bash
python -m venv venv
# Hoặc: py -3.11 -m venv venv (để trỏ đích danh phiên bản, NÊN DÙNG)
venv\Scripts\activate
pip install -r requirements.txt
```

! Nếu gặp lỗi "cannot be loaded because ... this system", coi phần Troubleshooting.

Kiểm tra nhanh:

```bash
python --version
python -c "import numpy, scipy, sympy, matplotlib; print('OK')"
```

## 3. Part 2 – Manim (Rendering Video)

-> Chỉ dành cho hệ điều hành Linux/WSL.

```bash
sudo apt update
sudo apt install texlive texlive-latex-extra

python -m venv venv
source venv/bin/activate

pip install -r requirements-manim.txt
```

- render video:

```bash
manim src/part2/manim_demo.py SceneName -pqh
```

## 4. Ghi chú

- Ghi chú về Manim và hệ thống
- LaTeX (texlive) cần thiết nếu dùng MathTex / Tex
- Không yêu cầu cài ffmpeg riêng cho Manim 0.20.1
- Không cần toàn bộ nhóm cài Manim

## 5. Troubleshooting

### 5.1. Python sai phiên bản

Kiểm tra

```bash
py -0
```

Tạo venv đúng version:

```bash
py -3.11 -m venv venv
```

### PowerShell chặn script

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
venv\Scripts\Activate.ps1
```
