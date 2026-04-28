= Phần 1: Phép khử Gauss và Các Ứng dụng

== Hướng cài đặt thuật toán

Trong phần này, nhóm tập trung xây dựng các hàm nền tảng để xử lý ma trận mà không sử dụng các trình giải sẵn của thư viện bên ngoài. Mã nguồn được tổ chức trong file gaussian.py với luồng xử lý chặt chẽ từ biến đổi sơ cấp đến các ứng dụng phức tạp hơn.

=== Các hàm chức năng chính

- gaussian_eliminate(A, b): Đây là hàm cốt lõi thực hiện đưa ma trận tăng cường $[A|b]$ về dạng bậc thang dòng (REF). Nhóm đã cài đặt kỹ thuật Partial Pivoting (chọn phần tử chốt lớn nhất về trị tuyệt đối) để tránh lỗi chia cho $0$ và giảm thiểu sai số làm tròn. Hàm trả về ma trận sau khi khử, số lần hoán đổi dòng (biến s) và vị trí các cột pivot.

- back_substitution(U, c): Thực hiện giải hệ phương trình tam giác trên bằng cách tính toán ngược từ dưới lên. Hàm này xử lý linh hoạt các trường hợp có biến tự do để đưa ra công thức nghiệm tổng quát.

- determinant(A): Tính định thức thông qua tích các phần tử trên đường chéo chính của ma trận sau khi khử Gauss: $det(A) = (-1)^s dot product(u_(i i))$.

- inverse(A): Tìm ma trận nghịch đảo bằng thuật toán Gauss-Jordan, đưa ma trận ghép $[A | I]$ về dạng $[I | A^(-1)]$.

- rank_and_basis(A): Rút ra thông tin về hạng của ma trận (số lượng pivot) và xác định cơ sở của các không gian con (Column Space, Row Space, Null Space).

- verify_solution(A, x, b): Hàm hậu kiểm sử dụng thư viện NumPy để so sánh kết quả tự cài đặt, đảm bảo độ chính xác của thuật toán.

== Kiểm chứng và kết quả

Để chứng minh tính ổn định và chính xác của thuật toán, nhóm đã thực hiện kiểm thử trên 5 kịch bản tiêu biểu từ file Jupyter Notebook.

#table(
columns: (auto, 1fr, 1.5fr, 1fr),
inset: 10pt,
align: horizon,
[Case], [Mục đích kiểm tra], [Hàm liên quan], [Kết luận chính],
[1], [Hệ vuông, cần đổi dòng], [gaussian_eliminate, inverse], [Pivoting hoạt động tốt],
[2], [Hệ suy biến, tương thích], [determinant, rank_and_basis], [Rank < n, det = 0],
[3], [Hệ vô nghiệm], [gaussian_eliminate], [Phát hiện hàng mâu thuẫn],
[4], [Hệ chữ nhật (vô số nghiệm)], [back_substitution, basis], [Tìm đúng biến tự do],
[5], [Hệ ill-conditioned], [Tính ổn định số học], [Sai số cực thấp],
)

=== Phân tích chi tiết các trường hợp

Case 1: Ma trận khả nghịch và bắt buộc đổi dòng
Ma trận $A_1$ có phần tử đầu tiên bằng $0$, bắt buộc thuật toán phải thực hiện hoán đổi dòng:
$A_1 = mat(0, 1, 2; 1, 2, 3; 2, 1, 1), b_1 = mat(4; 7; 4)$
Kết quả ghi nhận: Thuật toán đã chọn dòng 3 (có giá trị $2$) đưa lên làm pivot. Hệ được giải ra nghiệm duy nhất, định thức $det(A_1) = 2$ và ma trận nghịch đảo khớp hoàn toàn với kết quả từ NumPy.

Case 2: Ma trận vuông suy biến nhưng hệ vẫn tương thích
$A_2 = mat(1, 2, 3; 2, 4, 6; 1, 1, 1), b_2 = mat(3; 6; 2)$
Ở trường hợp này, dòng 2 phụ thuộc tuyến tính vào dòng 1. Kết quả kiểm chứng cho thấy $det(A_2) = 0$, hàm inverse(A_2) báo lỗi ma trận không khả nghịch, và rank_and_basis xác định hạng bằng $2$. Hệ có vô số nghiệm với một biến tự do.

Case 3: Hệ vô nghiệm (Inconsistent)
$A_3 = mat(1, 1, 1; 2, 2, 2; 1, -1, 0), b_3 = mat(3; 7; 1)$
Sau khi thực hiện khử Gauss, tại dòng 2 của ma trận tăng cường xuất hiện dạng $[0, 0, 0 | 1]$. Vì $0 eq.not 1$, thuật toán đã dừng và kết luận hệ vô nghiệm, chứng minh nhánh xử lý inconsistent hoạt động chính xác.

Case 4: Hệ chữ nhật có vô số nghiệm
$A_4 = mat(1, 2, 3; 2, 4, 6), b_4 = mat(4; 8)$
Trường hợp này chứng minh khả năng tìm "free columns" và "nullspace basis". Thuật toán đã xác định được các cột tự do và đưa ra nghiệm tổng quát dưới dạng vector, cho thấy ý nghĩa toán học của việc cài đặt không chỉ dừng lại ở các hệ vuông đơn giản.

Case 5: Hệ ill-conditioned (Pivot cực nhỏ)
$A_5 = mat(10^(-10), 1; 1, 1), b_5 = mat(1; 2)$
Với $A_5$, nếu không sử dụng Partial Pivoting, sai số làm tròn khi chia cho $10^(-10)$ sẽ làm hỏng kết quả. Nhóm ghi nhận nhờ việc hoán đổi dòng, thuật toán duy trì được độ ổn định số học tuyệt đối, nghiệm thu được có sai số residual xấp xỉ $0$.

== Nhận xét rút ra từ Phần 1

Thông qua quá trình cài đặt và kiểm thử, nhóm đã rút ra các nhận định quan trọng:

1. Tầm quan trọng của Pivoting: Đây không chỉ là bước kỹ thuật mà là yếu tố sống còn để thuật toán chạy được trên máy tính với số thực dấu phẩy động.

2. Tính đa dạng của hệ phương trình: Việc xử lý triệt để các trường hợp vô nghiệm và vô số nghiệm giúp bộ code có khả năng ứng dụng thực tế cao hơn.

3. Sự tương quan: Kết quả từ các hàm tự viết luôn được đối chiếu với NumPy, giúp nhóm tự tin vào "core" tính toán trước khi chuyển sang các phần trực quan hóa phức tạp hơn.