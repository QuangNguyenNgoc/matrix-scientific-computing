# Bản tổng quan
## 1. Tổng quan từ tài liệu:
### 1.1 Nhóm kĩ thuật về Toán:
- Phép khử Gauss
- Phân rã ma trận, chéo hóa
- Ổn định số học và chi phí tính toán
### 1.2 Nhóm kĩ thuật về code:
- Python 3.10: ngôn ngữ lập trình chính. Các thư viện xem phần `giới thiệu đồ án`. Dưới mỗi phần sẽ có mục `yêu cầu cài đặt Python`  có thêm yêu cầu cài đặt. (ví dụ có : "Sinh viên cài đặt từ đầu (không dùng NumPy/SciPy/SymPy)")
- Manim stable v.20.1: trực quan bằng video.

### 1.3 Tóm tắt mỗi phần
1. Phần chính
	- Tóm tắt yêu cầu
	- Tổng quan lý thuyết
	- Yêu cầu chính... viết code theo hàm cho sẵn, code manim render video,...
## Yêu cầu cho nhóm:
**Thống nhất:** hệ điều hành Windows (lưu ý manim). Lưu trữ phiên bản code bằng Github, các loại thư mục báo cáo khác như video, pdf trên google drive. Viết báo cáo bằng Markdown (kết hợp trong file jupyter notebook). Thống nhất về thư viện (dù muốn test trên máy, vẫn nên nhớ tạo venv):
```markdown
Python: 3.10.x
numpy: 1.26.x
scipy: 1.11.x
matplotlib: 3.8.x
jupyter: 1.0.x
// khác, chỉ dành cho task video
manim: 0.18.1
```
**!** manim chạy tốt trên WSL/Linux, vì tính ổn định "bắt buộc" dùng WSL/Linux khi làm task video.
### 1.1 Python
- Cố gắng thành thạo cơ bản cơ sở lập trình, clean code với OOP.
-  `NumPy` là nền tảng tính toán số. `Matplotlib` dùng `NumPy` array làm input nên cần nắm `NumPy` trước.
- **Kĩ năng**: Xử lí ngoại lệ `(try...except)`. Type hinting `def function(a: int) -> str:` để trực quan dữ liệu.
- Sử dụng `venv` (hoặc `conda`). `requirements.txt` để cài đặt, quản lí thư viện "dùng chung" cho nhóm. Sai lệch phiên bản đôi lúc gây lỗi. (cái này tui sẽ tìm hiểu/viết sau).
- **Cách thư viện nâng cao như Matplotlib có thể vừa học vừa làm khi đã có kiến thức nền **
### 1.2 DevOps
- git/Github: thành thạo làm việc trên commit, branch (git) và remote, pull request (GitHub). 
	- **Một số yêu cầu khác:** tham gia repos (tạo sau), clone code về, code trên local (git). 
	- Mỗi phần làm code của mọi người khi được yêu cầu nằm trên một branch tự tạo.

### Bonus: lí do và bổ sung
- **? Cần thiết đồng bộ phiên bản python, hệ điều hành?**
-> Bắt buộc, cũng tương tự với các thư viện khác nằm trong `venv`, `requirements.txt`. 
	- Có một số hàm/lệnh ở phiên bản cũ không có, nhưng ở phiên bản mới hơn thì có hay cách thực thi khác nhau.
	-  Ví dụ : `Matplotlib` ở bản cũ, một số thuộc tính truy cập được trực tiếp. Nhưng ở bản mới, các thuộc tính được gom chúng vào các đối tượng con (ví dụ: `ax.set_title()` ). Hậu quả code ở phiên bản mới sẽ không chạy được ở bản cũ.
-> Ở hệ điều hành, một số "kí tự" ví dụ dấu xuống dòng ở Windows và Linux khác nhau khi Windows dùng `\r\n`, Linux lại dùng `\n`. Hay case đơn giản hơn về **File paths** là Windows dùng `"\"` còn Linux thì `"/"`.
-> `venv` là "môi trường độc lập để chứa thư viện vào một project độc lập. (lưu ý .gitignore). `requirements.txt` là danh mục thư viện để biết tải về.
- **Làm gì trên Github?** 
-> Chỉ đơn giản đưa code lên github là được. 
	- **(OPTION)** Gợi ý là khi làm việc với git và github, nên dùng SSH key để thao tác giữa local và remote, nếu dùng vscode thì nhớ có tạo keys và lưu trong máy, nếu `git remote -v` được tức bước setup đã chuẩn. 

## Lộ trình làm việc chính như sau:
**Quan trọng: Khi mà các bước setup thư viện, môi trường (venv), git/github đã hoàn tất**
1. Nhận task -> Task sẽ được giao cụ thể sau, tương ứng với từng phần của đồ án.
....
2. Nếu có code, thì nhớ làm trên branch (git), pull request khi hoàn thành (có vẻ tui sẽ thêm 1 file để kĩ hơn về git/github nếu mn có thắc mắc hoặc chưa quen).
	- Tên branch nên đặt rõ theo task: ví dụ part1/gaussian-eliminate, part2/lu-decomposition, part3/benchmark,...
	- Không cần quan tâm commit sạch, pull request đạt yêu cầu task, viết nội dung như báo cáo với tôi là được. 
	- Không nên commit trên branch `main` nha! 
	- Task (tương ứng branch) cố gắng sẽ không phụ thuộc nhau. Nên ai đảm nhiệm task nào thì chỉ được sửa đổi file code cần cho task. Tránh trường hợp `conflict`  .
3. Hoàn thành rồi thì nhớ nhắn trên nhóm. Có thể trao đổi vấn đề gặp phải với tui. 


## Tóm tắt những thứ sẽ có tiếp:
- Github repos cho mọi người làm chung.
- Google Drive (chưa cần quan trọng hiện tại) : chủ yếu để nạp video, pdf. Hoặc có thể mọi người up tài liệu tham khảo chung.
- Các file tài liệu tham khảo:
	- git/github workflow: chủ yếu cách làm việc. Bộ môn **tư duy tính toán** có dạy Git/Github mọi người có thể tham khảo tài liệu thầy/cô.
- Task: tôi sẽ lọc trong file đồ án...
- `requirements.txt` và `venv`: các thư viện chính xác cho mọi người làm việc.


## Tham khảo chút....
### Git
[Why-git](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control): lí do tại sao là git? Hiểu về công cụ quản lí phiên bản siêu mạnh này :3
[SSH-key-gen](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent): liên kết git và github bằng SSH key. Mạnh và an toàn rất nhiều so với thao tác HTTPS cổ điển.
[git-commit](https://cbea.ms/git-commit): dù không quan tâm lắm về commit, nhưng commit message đẹp - chuẩn chỉ giúp bản thân làm việc tốt hơn, ví dụ "gợi lại" mình đã làm gì lúc đó. Mà mình chỉ cần đọc message là hiểu ngay!

### Python, trực quan hóa
[@3blue1brown](https://www.youtube.com/@3blue1brown) : kênh youtube chuyên gia về trực quan Toán Học.

### WSL
[wsl2.md](https://github.com/TheOdinProject/curriculum/blob/main/foundations/installations/installation_guides/linux/wsl2.md): cách tạo WSL, nên cài cả WSL trên cả vscode.


## ....
`.gitattributes`
```yaml
* text=auto eol=lf 
  *.py text eol=lf 
  *.ipynb text eol=lf
```
`.gitignore`
```yaml
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
media/          // video render
*.mp4
*.pdf
```