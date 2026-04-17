#import "../helpers/metadata.typ": codeblock
= Phép khử Gauss và ứng dụng
Phần này tập trung vào phép khử Gauss và các ứng dụng trực tiếp của nó trong đại số tuyến tính số. Thay vì chỉ sử dụng phép khử Gauss để giải hệ phương trình tuyến tính, nhóm khai thác cùng một ý tưởng biến đổi dòng để xây dựng các chức năng quan trọng khác như tính định thức, tìm ma trận nghịch đảo, xác định hạng và mô tả các cơ sở liên quan của ma trận.

Vì các bài toán này có chung nền tảng toán học nhưng khác nhau ở đầu ra cần thu được, nhóm tổ chức phần cài đặt thành các hàm riêng biệt nhằm giúp việc kiểm thử, giải thích và tái sử dụng thuật toán được rõ ràng hơn.

== Cài đặt thuật toán
// === Các hàm phu trợ
// Các hàm phụ trợ có tác dụng chuẩn hóa dữ liệu đầu vào và thao tác ma trận. 
// - Nguồn: `utils.py`.
// - Bao gồm:
//     - `_to_matrix` : 
//     - `_to_vector` :
//     - `_shape` :
//     - `_copy_matrix` :
//     - `identity` :
//     - `_clean_small_entries` :
//     - `_augment` :
//     - `_swap_rows` :
=== `gaussian_eliminate(A, b)`
*Mục tiêu*: giải hệ $A x = b$ bằng phép khử Gauss và phân loại loại nghiệm theo 3 trường hợp: có nghiệm duy nhất, có vô số nghiệm hoặc vô nghiệm.

*Đầu vào*: ma trận hệ số kích thước `m x n` (kí hiệu: A), vector vế phải kích thước m (kí hiệu: b), ngưỡng nhận diện số gần bằng 0 (`kí hiệu: eps`, tùy chọn với giá trị mặc định $10^(-12)$).

*Đầu ra*: ma trận tăng cường ở dạng REF, một cấu trúc `solution_info` mô tả loại nghiệm và nội dung nghiệm, cùng với `swap_count` là số lần hoán đổi dòng.

*Ý tưởng thuật toán:*
Trước hết, hệ được viết dưới dạng ma trận tăng cường $[A | b]$. Thuật toán thực hiện khử Gauss có partial pivoting: ở mỗi cột, chọn phần tử có trị tuyệt đối lớn nhất làm pivot để giảm rủi ro chia cho số quá nhỏ. Sau khi khử về dạng REF, hệ được phân loại như sau:

- nếu xuất hiện hàng $[0, dots, 0 | c]$ với $c != 0$, hệ vô nghiệm;
- nếu số cột pivot bằng số ẩn, hệ có nghiệm duy nhất;
- nếu còn cột tự do, hệ có vô số nghiệm.

*Cách cài đặt:*
Trong code, ma trận tăng cường được tạo bằng `_augment`. Bước khử tiến được thực hiện trong `_forward_elimination_ref`, đồng thời theo dõi `pivot_columns`, `swap_count` và cảnh báo nếu pivot quá nhỏ. Từ kết quả khử, quá trình phân nhánh theo từng loại nghiệm:
- nếu xuất hiện hàng mâu thuẫn thì trả về hệ vô nghiệm;
- Nếu hệ có nghiệm duy nhất, chương trình tách hệ tam giác trên bằng `_extract_upper_system` rồi chuyển cho `back_substitution`.
- Nếu hệ có vô số nghiệm, chương trình dùng `_rref` và `_build_general_solution_from_rref` để dựng nghiệm tổng quát.

Cách tổ chức này giúp phần cài đặt bám sát đúng ba trường hợp đã nêu trong phần ý tưởng thuật toán, đồng thời làm cho từng nhánh xử lý có thể được kiểm tra độc lập

=== `back_substitution(U, c, eps)`
*Mục tiêu:*
Giải hệ tam giác trên $U x = c$ trong trường hợp hệ có nghiệm duy nhất.

*Đầu vào:*
Ma trận tam giác trên $U$, vector vế phải $c$, và ngưỡng $e p s $.

*Đầu ra:*
Vector nghiệm $x$.

*Ý tưởng thuật toán:*
Thực hiện thế ngược từ hàng cuối lên hàng đầu. Ở mỗi bước, một ẩn được tính dựa trên các ẩn đã biết trước đó.

*Cách cài đặt:*
Hàm duyệt chỉ số hàng từ cuối về đầu, tính phần tổng các hạng tử đã biết rồi suy ra giá trị của ẩn hiện tại. Nếu phần tử trên đường chéo chính quá nhỏ hoặc bằng 0, hàm báo lỗi vì không thể tiếp tục thế ngược.

=== `determinant(A, eps)`
*Mục tiêu:*
Tính định thức của ma trận vuông.

*Đầu vào:*
Ma trận vuông A và ngưỡng eps.

*Đầu ra:*
Giá trị định thức của ma trận.

*Ý tưởng thuật toán:*
Đưa ma trận về dạng tam giác trên bằng phép khử Gauss. Khi đó, định thức được tính bằng tích các phần tử trên đường chéo. Nếu có đổi dòng, dấu của định thức thay đổi theo số lần hoán đổi.

*Cách cài đặt:*
Hàm tái sử dụng `_forward_elimination_ref` để nhận ma trận sau khử và `swap_count`. Sau đó tính tích các phần tử đường chéo và nhân với dấu $(-1)^s$. Nếu đầu vào không phải ma trận vuông, hàm báo lỗi.

=== inverse(A, eps)
*Mục tiêu:*
Tính ma trận nghịch đảo $A^(-1)$.

*Đầu vào:*
Ma trận vuông A và ngưỡng eps.

*Đầu ra:*
Ma trận nghịch đảo của A.

*Ý tưởng thuật toán:*
Dùng phương pháp `Gauss-Jordan` trên ma trận ghép $[A | I]$. Nếu đưa được vế trái về ma trận đơn vị, thì vế phải chính là $A^(-1)$.

*Cách cài đặt:*
Hàm ghép $A$ với ma trận đơn vị cùng kích thước. Với mỗi cột, chương trình chọn pivot phù hợp, đổi dòng nếu cần, chuẩn hóa dòng pivot rồi khử tất cả các dòng còn lại. Sau khi hoàn tất, phần bên phải của ma trận ghép được tách ra làm ma trận nghịch đảo. Nếu không chọn được pivot hợp lệ, hàm báo lỗi do ma trận suy biến.

=== `rank_and_basis(A, eps)`

*Mục tiêu:*
Tính hạng của ma trận và xác định các cơ sở liên quan.

*Đầu vào:*
Ma trận A và ngưỡng eps.

*Đầu ra:*
Một cấu trúc dữ liệu chứa `rank, pivot_columns`, `free_columns`, `column_space_basis`, `row_space_basis` và `null_space_basis`.

*Ý tưởng thuật toán:*
Từ dạng RREF, số cột pivot cho biết hạng ma trận. Các cột pivot của ma trận gốc tạo thành cơ sở không gian cột; các dòng khác 0 của RREF tạo thành cơ sở không gian dòng; các cột tự do được dùng để dựng cơ sở không gian nghiệm.

*Cách cài đặt:*
Hàm gọi `_rref` để lấy ma trận rút gọn và danh sách `pivot_columns`. Từ đó, chương trình suy ra `free_columns` và lần lượt dựng các basis tương ứng. Đây là bước chuyển trực tiếp từ khái niệm toán học sang cấu trúc dữ liệu có thể dùng tiếp trong code.

=== `verify_solution(A, x, b, tol)`
*Mục tiêu:*
Kiểm chứng nghiệm hoặc thông tin nghiệm do phần cài đặt chính trả về.

*Đầu vào:*
Ma trận A, nghiệm hoặc solution_info, vector b, và ngưỡng tol.

*Đầu ra:*
Một cấu trúc chứa is_close, residual_norm, relative_residual và nghiệm tham chiếu từ NumPy.

*Ý tưởng thuật toán:*
Không tham gia vào phần tính toán lõi. Hàm này chỉ dùng để đối chiếu kết quả và đo mức độ sai số thông qua residual.

*Cách cài đặt:*
Nếu đầu vào là nghiệm duy nhất hoặc nghiệm riêng của hệ vô số nghiệm, hàm chuyển sang mảng NumPy để kiểm tra Ax≈b. Nếu đầu vào thuộc nhánh vô nghiệm, hàm báo lỗi thay vì cố kiểm tra một nghiệm không tồn tại.