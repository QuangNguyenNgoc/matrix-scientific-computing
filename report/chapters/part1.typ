#set text(font: "Arial", size: 11pt)
#set heading(numbering: "1.1.")
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))

#let rank = math.op("rank")

#align(center)[
#text(size: 14pt)[Phần 1 - Phép khử Gauss và Các ứng dụng]
]

#v(1em)

= Hướng cài đặt thuật toán
Trong phần này, nhóm đã thực hiện cài đặt các hàm cốt lõi phục vụ giải quyết hệ phương trình và phân tích ma trận không sử dụng các hàm giải sẵn của thư viện. Các hàm được chia vào các file chuyên biệt để dễ quản lý:

gaussian.py: Chứa hàm gaussian_eliminate thực hiện khử Gauss với chiến lược chọn phần tử chốt một phần (partial pivoting). Ngoài ra còn có back_substitution để giải hệ tam giác trên và `_rref` để đưa ma trận về dạng bậc thang rút gọn.

determinant.py: Cài đặt hàm determinant tính định thức dựa trên tích đường chéo của ma trận sau khi khử, có xét đến số lần đổi dòng để quyết định dấu.

inverse.py: Hàm inverse sử dụng phương pháp Gauss-Jordan để tìm ma trận nghịch đảo bằng cách biến đổi đồng thời ma trận $[A | I]$.

rank_basis.py: Hàm rank_and_basis thực hiện tính hạng của ma trận và trích xuất cơ sở cho các không gian con (Column Space, Row Space, Null Space).

verify.py: Sử dụng thư viện NumPy để kiểm chứng sai số thặng dư (residual) nhằm đảm bảo tính ổn định số học.

= Kiểm chứng và Kết quả
Dưới đây là các trường hợp kiểm thử tiêu biểu được thực hiện để đánh giá độ chính xác và khả năng xử lý các tình huống đặc biệt của thuật toán.

== Bảng tóm tắt các Trường hợp kiểm thử

#text(size: 9pt)[
  #table(
    columns: (0.9cm, 4.2cm, 4.2cm, 5.2cm),
    inset: 5pt,
    stroke: 0.5pt,
    align: horizon,
    [*Trường hợp*], [*Mục đích*], [*Hàm được kiểm tra*], [*Kết luận chính*],
    [1], [Near-zero pivot nhưng hệ vẫn giải tốt nhờ partial pivoting], [`gaussian_eliminate`, `back_substitution`, `determinant`, `inverse`, `verify_solution`], [Có đổi dòng, nghiệm duy nhất, residual rất nhỏ],
    [2], [Hệ có vô số nghiệm do các dòng phụ thuộc tuyến tính], [`gaussian_eliminate`, `rank_and_basis`, `verify_solution`], [Phân loại `infinite`, tìm được nghiệm riêng và cơ sở null space],
    [3], [Hệ vô nghiệm do xuất hiện dòng mâu thuẫn sau khử Gauss], [`gaussian_eliminate`], [Phân loại `inconsistent`, không ép tạo nghiệm],
    [4], [Hệ ill-conditioned có pivot gần 0], [`gaussian_eliminate`, `verify_solution`], [Có nghiệm duy nhất nhưng xuất hiện warning về độ ổn định số học],
  )
]

== Chi tiết

=== Trường hợp 1: Near-zero pivot

Kiểm tra khả năng chọn phần tử chốt một phần. Phần tử đầu tiên của ma trận có độ lớn rất nhỏ, cụ thể là $10^(-10)$, nên nếu thuật toán khử trực tiếp theo thứ tự dòng ban đầu thì phép chia cho pivot nhỏ có thể làm sai số tăng. Nhờ partial pivoting, chương trình đổi dòng để chọn pivot lớn hơn trước khi khử.

Đề bài: giải hệ $A_1 x = b_1$, với

$A_1 = mat(
  10^(-10), 2.34567, -1.23456;
  3.5, -4.2, 1.125;
  2.25, 1.33333, 5.75
)$

$b_1 = vec(1.2345, -2.3456, 3.4567)$

Kết quả:

- Ma trận bậc thang của ma trận tăng cường:

  $mat(
    3.5000, -4.2000, 1.1250, -2.3456;
    0.0000, 4.0333, 5.0268, 4.9646;
    0.0000, 0.0000, -4.1580, -1.6528
  )$

- `solution_info["type"] = "unique"`.
- Số lần hoán đổi dòng: `swap_count = 2`.
- Nghiệm thu được từ `back_substitution`:

  $x = vec(0.0847, 0.7355, 0.3975)$

- Định thức:

  $det(A_1) = -58.6970$

- Ma trận nghịch đảo:

  $A_1^(-1) = mat(
    0.4370, 0.2578, 0.0434;
    0.2997, -0.0473, 0.0736;
    -0.2405, -0.0899, 0.1399
  )$

- Kết quả kiểm chứng: `is_close = True`, `residual_norm = 0.0000`, `relative_residual = 0.0000`.

Ý nghĩa: Trường hợp này cho thấy partial pivoting hoạt động đúng vì chương trình đã đổi dòng khi pivot ban đầu quá nhỏ. Nghiệm từ `back_substitution` trùng với nghiệm trong `solution_info`, đồng thời residual rất nhỏ, nên kết quả giải hệ là nhất quán.

=== Trường hợp 2: Hệ có vô số nghiệm

Kiểm tra nhánh xử lý hệ tương thích nhưng không có nghiệm duy nhất. Ma trận hệ số có các dòng phụ thuộc tuyến tính, vì vậy số pivot nhỏ hơn số ẩn và xuất hiện biến tự do.

Đề bài: giải hệ $A_2 x = b_2$, với

$A_2 = mat(
  1.2, 2.4, -0.6, 3.0;
  2.4, 4.8, -1.2, 6.0;
  0.6, 1.2, -0.3, 1.5
)$

$b_2 = vec(3.6, 7.2, 1.8)$

Kết quả:

- Ma trận bậc thang của ma trận tăng cường:

  $mat(
    2.4000, 4.8000, -1.2000, 6.0000, 7.2000;
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000;
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000
  )$

- `solution_info["type"] = "infinite"`.
- Số lần hoán đổi dòng: `swap_count = 1`.
- Hạng của ma trận: `rank = 1`.
- Cột pivot: `pivot_columns = [0]`.
- Cột tự do: `free_columns = [1, 2, 3]`.
- Một nghiệm riêng:

  $x_p = vec(3.0000, 0.0000, 0.0000, 0.0000)$

- Cơ sở của null space:

  $v_1 = vec(-2.0000, 1.0000, 0.0000, 0.0000)$

  $v_2 = vec(0.5000, 0.0000, 1.0000, 0.0000)$

  $v_3 = vec(-2.5000, 0.0000, 0.0000, 1.0000)$

- Dạng nghiệm tổng quát:

  $x = vec(3.0000, 0.0000, 0.0000, 0.0000) + t_1 vec(-2.0000, 1.0000, 0.0000, 0.0000) + t_2 vec(0.5000, 0.0000, 1.0000, 0.0000) + t_3 vec(-2.5000, 0.0000, 0.0000, 1.0000)$

- RREF của ma trận tăng cường:

  $mat(
    1.0000, 2.0000, -0.5000, 2.5000, 3.0000;
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000;
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000
  )$

- Kết quả kiểm chứng với nghiệm riêng: `is_close = True`, `residual_norm = 0.0000`, `relative_residual = 0.0000`.

Ý nghĩa: Chương trình phân loại đúng hệ có vô số nghiệm, xác định được pivot column, free columns, nghiệm riêng và cơ sở null space. Việc `verify_solution` cho residual rất nhỏ chứng minh nghiệm riêng mà chương trình trả về thỏa mãn hệ phương trình.

=== Trường hợp 3: Hệ vô nghiệm

Kiểm tra nhánh phát hiện hệ không tương thích. Sau khi khử Gauss, ma trận tăng cường xuất hiện một dòng có toàn bộ hệ số bằng 0 nhưng vế phải khác 0, tương ứng với mệnh đề sai dạng $0 = c$, trong đó $c != 0$.

Đề bài: giải hệ $A_3 x = b_3$, với

$A_3 = mat(
  1, 1, 1;
  2, 2, 2;
  1, -1, 0
)$

$b_3 = vec(3, 7, 1)$

Kết quả:

- Ma trận bậc thang của ma trận tăng cường:

  $mat(
    2.0000, 2.0000, 2.0000, 7.0000;
    0.0000, -2.0000, -1.0000, -2.5000;
    0.0000, 0.0000, 0.0000, -0.5000
  )$

- `solution_info["type"] = "inconsistent"`.
- Cột pivot: `pivot_columns = [0, 1]`.
- Số lần hoán đổi dòng: `swap_count = 2`.

Ý nghĩa: cho thấy chương trình nhận diện đúng hệ vô nghiệm. Vì hệ không tồn tại nghiệm, báo cáo không nên gọi `back_substitution`, `inverse` hoặc `verify_solution`.

=== Trường hợp 4 - Hệ ill-conditioned và warning về pivot gần 0

Ma trận gần suy biến vì hai dòng gần như phụ thuộc tuyến tính. Hệ vẫn có nghiệm duy nhất, nhưng trong quá trình khử xuất hiện pivot rất nhỏ.

Đề bài: giải hệ $A_4 x = b_4$, với

$A_4 = mat(
  1.0, 1.0;
  1.0, 1.0 + 10^(-10)
)$

$b_4 = vec(2.0, 2.0 + 10^(-10))$

Kết quả:

- Ma trận bậc thang của ma trận tăng cường sau khi làm tròn 4 chữ số thập phân:

  $mat(
    1.0000, 1.0000, 2.0000;
    0.0000, 0.0000, 0.0000
  )$

- `solution_info["type"] = "unique"`.
- Số lần hoán đổi dòng: `swap_count = 0`.
- Nghiệm:

  $x = vec(1.0000, 1.0000)$

- Warning: `pivot is near zero; the system may be ill-conditioned`.
- Kết quả kiểm chứng: `is_close = True`, `residual_norm = 0.0000`, `relative_residual = 0.0000`.

Ý nghĩa: Chương trình không chỉ trả nghiệm mà còn nhận diện được rủi ro khi pivot quá nhỏ. Việc dòng thứ hai nhìn như toàn số 0 là do kết quả đang được làm tròn tới 4 chữ số thập phân; về mặt tính toán, chương trình vẫn phát hiện pivot rất nhỏ và đưa ra warning.

= Kết luận phần 1
Nhóm đã hoàn thành việc cài đặt bộ công cụ xử lý ma trận cơ bản. Kết quả thực nghiệm trên các test Trường hợp từ đơn giản đến phức tạp (suy biến, vô nghiệm, ill-conditioned) đều khớp với lý thuyết toán học và kết quả kiểm chứng từ thư viện NumPy. Việc áp dụng Partial Pivoting đã giúp tăng đáng kể độ ổn định cho các bài toán thực tế.