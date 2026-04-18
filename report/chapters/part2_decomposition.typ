= Phân rã ma trận và trực quan hóa với Manim
Trong phàn này, nhóm tập trung vào kỹ thuật phân rã ma trận và chéo hóa, trong đó nhóm lựa chọn phân rã kỳ dị SVD làm kỹ thuật chính. Lý do "..."

Ngoài ra, nhóm có dùng Manim để trực quan hóa các kỹ thuật trên để có thể theo dõi quá trình phân rã và chéo hóa thông qua bài toán.

== Ý tưởng chính
*Chéo hóa (Diagonalization)*: Áp dụng Leverrier-Faddeev tìm phương trình đặc trưng rồi giải nghiệm đa thức bằng phương pháp lặp song song Durand-Kerner. Sau khi có $lambda$, thuật toán đưa về giải hệ thuần nhất bằng phương pháp Khử Gauss (với *Partial Pivoting* chọn dòng có trị tuyệt đối lớn nhất để khử làm mốc, đảm bảo tránh chia cho 0 và giảm thiểu sai số tính toán).
tính chất trực giao vuông góc tuyệt đối.

*Phân rã SVD*: 
-Tính $A^T A$, mượn lại hàm `findEigen` bên chéo hóa để lấy các giá trị trị riêng $lambda_i >= 0$.
- Trị kỳ dị $sigma_i = sqrt(lambda_i)$.
- Tính các cột của $U$ qua công thức $u_i = (A dot v_i) / sigma_i$.

*Lưu ý tính trực giao (Orthogonality) và Liên tục*: Vì hỗ trợ ma trận không vuông $m times n$, hoăc khi có $sigma_i = 0$ (Null space), ma trận $U$ có xu hướng bị thiếu cột. Code đã tự động kết hợp chèn chuỗi trực giao hóa *Gram-Schmidt* đối diện với các vector cơ sở gốc (Standard Basis $e_k$) để sinh đủ các cột còn thiếu, giúp ma trận $U$ bảo toàn 100% kích cỡ $m times m$ và tính chất trực giao vuông góc tuyệt đối.
