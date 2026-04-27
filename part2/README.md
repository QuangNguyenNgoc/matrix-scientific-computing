## Link video demo Manim
https://youtu.be/sWpLmDTU0R0

## Lưu ý liên quan đến dependencies
- Phần core gồm `decomposition.py` và `diagonalization.py` sử dụng các thư viện được liệt kê trong `requirements.txt` (file chính).
- Mặt khác, video Manim (`manim_scene.py`) sử dụng `requirements-manim.txt` và sử dụng **Linux** làm môi trường chính (do nhiều thư viện chỉ hỗ trợ cho hệ điều hành này).
- Phương án cài đặt tốt nhất cho manim(cho Linux):
```bash
# Tạo môi trường
python -m venv venv-manim
source venv-manim/bin/activatetrường

# Cài thư viện Python
pip install -r part2/requirements-manim.txt

# Cài các dependencies hỗ trợ
sudo apt install build-essential python3-dev pkg-config \ libcairo2-dev libpango1.0-dev ffmpeg dvisvgm
```
- Lưu ý cách trên tạo môi trường cách biệt so với các file khác(Core). Tức là nếu thử demo code part2 thì core code có thể dùng chung venv của cả 3 part, còn Manim thì tạo khác. 