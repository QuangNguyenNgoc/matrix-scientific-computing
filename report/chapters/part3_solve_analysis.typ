= *Phần 3:* Giải Hệ Phương Trình và Phân Tích Hiệu Năng

== Mục tiêu

Phần 3 của đồ án tập trung vào việc nối từ cơ sở lý thuyết của đại số tuyến tính số đến hành vi thực tế của thuật toán khi chạy trên máy tính. Mục tiêu của nhóm là đánh giá và so sánh ba phương pháp giải hệ phương trình tuyến tính gồm *khử Gauss có partial pivoting*, *phân rã LU có partial pivoting*, và *phương pháp lặp Gauss-Seidel* trên ba phương diện chính:

- *Chi phí tính toán*: khảo sát thời gian thực thi khi kích thước ma trận tăng dần, từ đó đối chiếu với độ phức tạp lý thuyết của từng phương pháp.
- *Độ chính xác của nghiệm*: đo mức độ sai lệch của nghiệm tính được thông qua residual error và solution error.
- *Độ ổn định số học*: quan sát phản ứng của thuật toán trên các lớp ma trận có bản chất rất khác nhau, đặc biệt là ma trận điều kiện tốt và điều kiện kém.

Thông qua phần này, nhóm muốn trả lời một câu hỏi thực tiễn hơn là chỉ mô tả thuật toán: *khi áp dụng vào dữ liệu cụ thể, phương pháp nào phù hợp hơn, nhanh hơn, và đáng tin cậy hơn về mặt số học*.

== Thiết kế thực nghiệm và tiêu chí đánh giá

Để việc so sánh phản ánh đúng bản chất của từng phương pháp, nhóm xây dựng hai nhóm thực nghiệm bổ sung cho nhau.

=== Nhóm thực nghiệm A: đo thời gian thực thi và sai số theo kích thước

Ở nhóm thực nghiệm thứ nhất, nhóm sinh các ma trận vuông *chéo trội nghiêm ngặt* với kích thước tăng dần
$ n in {50, 100, 200, 500, 1000}. $
Việc chọn ma trận chéo trội nhằm bảo đảm phương pháp Gauss-Seidel có điều kiện hội tụ rõ ràng, đồng thời tạo ra một môi trường công bằng để so sánh với hai phương pháp trực tiếp là Gauss và LU.

Với mỗi kích thước, nhóm chọn nghiệm chuẩn
$ x_"true" = (1,1,dots,1)^T $
và dựng vế phải theo công thức
$ b = A x_"true". $
Cách làm này cho phép kiểm tra trực tiếp chất lượng nghiệm trả về, vì nghiệm đúng đã được biết trước.

Mỗi thuật toán được chạy *5 lần* trên cùng một kích thước để lấy *thời gian thực thi trung bình*. Cách lặp lại nhiều lần giúp giảm ảnh hưởng của dao động môi trường thực thi và làm cho số liệu benchmark ổn định hơn.

=== Nhóm thực nghiệm B: phân tích ổn định số học

Ở nhóm thực nghiệm thứ hai, mục tiêu không còn là tốc độ mà là *độ nhạy của nghiệm trước điều kiện của ma trận*. Nhóm sử dụng hai lớp dữ liệu:

- *Ma trận Hilbert* với các kích thước
$ n in {3, 5, 8, 10, 12, 15}, $
đại diện cho lớp ma trận *điều kiện kém* (*ill-conditioned*), trong đó số điều kiện tăng rất nhanh theo kích thước.
- *Ma trận SPD ngẫu nhiên* với các kích thước
$ n in {5, 10, 20, 50, 100}, $
đóng vai trò nhóm đối chứng có điều kiện tốt hơn, giúp làm rõ sự khác biệt về ổn định số học.

Với mỗi ma trận, nhóm tiếp tục sử dụng nghiệm chuẩn $x_"true"$ để dựng vế phải $b = A x_"true"$, sau đó giải lại bằng ba phương pháp và so sánh sai số.

=== Cài đặt và nguyên tắc thực thi

Các solver trong Part 3 được cài đặt bằng *nested list thuần Python*, không sử dụng NumPy array trong phần lõi thuật toán. NumPy chỉ được dùng trong các bước sinh dữ liệu, tính chuẩn, tính số điều kiện và đối chiếu kết quả sau cùng. Điều này giúp giữ đúng tinh thần của đồ án: thư viện chỉ phục vụ *benchmark và verification*, không thay thế cho phần cài đặt thuật toán.

Trong ba solver được so sánh, *LU* được dùng như một phương pháp phân rã phục vụ bài toán giải hệ trong benchmark; mục tiêu của Part 3 ở đây là đánh giá hiệu năng của các solver tiêu biểu, chứ không lặp lại toàn bộ phạm vi lý thuyết của Part 2.

=== Các thước đo sử dụng

Để đánh giá toàn diện, nhóm sử dụng đồng thời nhiều chỉ số:

- *Average Runtime*: thời gian thực thi trung bình sau nhiều lần chạy.
- *Relative Residual Error*:
  $ (||A hat(x) - b||_2)/(||b||_2), $
 phản ánh mức độ thỏa mãn của nghiệm tính được đối với hệ phương trình ban đầu.
- *Solution Error*:
  $ (||hat(x) - x_"true"||_2)/(||x_"true"||_2), $
 phản ánh sai lệch thực sự của nghiệm tính toán so với nghiệm chuẩn.
- *Condition Number*:
  $ kappa(A), $
  dùng để giải thích mối quan hệ giữa cấu trúc ma trận và mức độ khuếch đại sai số.

Nhóm lưu toàn bộ kết quả benchmark dưới dạng `.csv`, sau đó sử dụng notebook phân tích để dựng bảng tổng hợp và biểu đồ trực quan.

== Kết quả và thảo luận

Từ các số liệu benchmark thu được, nhóm nhận thấy sự khác biệt rõ ràng giữa ba phương pháp cả về thời gian thực thi lẫn độ ổn định số học. Các quan sát dưới đây được rút ra từ dữ liệu tổng hợp và các biểu đồ phân tích đi kèm.

=== Thời gian thực thi và chi phí tính toán

Kết quả thực nghiệm A cho thấy hai phương pháp trực tiếp là *khử Gauss* và *LU* đều có xu hướng tăng thời gian rất nhanh khi kích thước ma trận tăng lên. Điều này phù hợp với phân tích lý thuyết rằng chi phí của hai phương pháp này tăng theo bậc xấp xỉ
$cal(O)(n^3). $

Ở các kích thước nhỏ, chênh lệch giữa ba phương pháp chưa rõ rệt. Tuy nhiên, khi \(n\) tăng lên các mức lớn hơn như \(500\) hoặc \(1000\), thời gian của Gauss và LU tăng mạnh và trở thành yếu tố chi phối. Trong khi đó, *Gauss-Seidel* cho thấy lợi thế đáng kể trên nhóm dữ liệu chéo trội, vì mỗi vòng lặp chỉ cần chi phí cỡ $cal(O)(n^3) $ và số vòng lặp quan sát được vẫn nằm trong ngưỡng chấp nhận được.

Kết quả này cho thấy trong môi trường dữ liệu thuận lợi cho hội tụ, phương pháp lặp có thể tiết kiệm thời gian đáng kể so với các phương pháp trực tiếp. Tuy vậy, lợi thế này không nên được hiểu như một kết luận tuyệt đối, vì hiệu quả của Gauss-Seidel còn phụ thuộc mạnh vào cấu trúc ma trận và tốc độ hội tụ thực tế.

#figure(
  image("../images/loglog_timing.png", width: 80%),
  caption: [Đồ thị log-log thời gian thực thi theo kích thước $n$]
) <fig:timing>

=== Độ chính xác của nghiệm trên dữ liệu điều kiện tốt

Trên nhóm ma trận *SPD ngẫu nhiên*, cả ba phương pháp đều cho nghiệm có sai số rất thấp. Residual error và solution error duy trì ở mức nhỏ, cho thấy trong điều kiện ma trận có cấu trúc thuận lợi và số điều kiện không quá lớn, các thuật toán đều hoạt động ổn định.

Điều này phù hợp với trực giác số học: khi bài toán được đặt trên một ma trận điều kiện tốt, sai số làm tròn trong quá trình tính toán không bị khuếch đại mạnh, nên nghiệm thu được vẫn bám sát nghiệm chuẩn.

=== Ảnh hưởng của số điều kiện: trường hợp ma trận Hilbert

Sự khác biệt rõ rệt nhất xuất hiện khi chuyển sang ma trận *Hilbert*. Đây là lớp ma trận nổi tiếng có số điều kiện tăng rất nhanh theo kích thước, nên thường được dùng để kiểm tra mức độ nhạy cảm của thuật toán đối với sai số làm tròn.

Kết quả thực nghiệm cho thấy khi $n$ tăng, *solution error* của các phương pháp trực tiếp bắt đầu tăng rõ rệt, dù trong nhiều trường hợp *relative residual* vẫn còn nhỏ. Điều này phản ánh đúng bản chất của bài toán điều kiện kém: một nghiệm có thể gần thỏa mãn phương trình $A hat(x) = b$, nhưng vẫn sai khác đáng kể so với nghiệm thực $x_"true"$. Nói cách khác, *residual nhỏ không đồng nghĩa với nghiệm đáng tin cậy* khi $kappa(A)$ lớn.

Đối với *Gauss* và *LU*, kỹ thuật partial pivoting giúp giảm bớt sai số làm tròn nhưng không thể loại bỏ hoàn toàn ảnh hưởng của điều kiện kém. Khi số điều kiện đủ lớn, các sai số số học vẫn bị khuếch đại và thể hiện rõ ở sai số nghiệm.

Đối với *Gauss-Seidel*, ma trận Hilbert vẫn là ma trận đối xứng xác định dương, nên về mặt lý thuyết phương pháp vẫn có cơ sở hội tụ. Tuy nhiên, kết quả thực nghiệm cho thấy tốc độ hội tụ và độ tin cậy của nghiệm suy giảm rõ rệt khi kích thước tăng. Trong các trường hợp khó, phương pháp có thể cần rất nhiều vòng lặp hoặc dừng ở trạng thái mà sai số nghiệm vẫn còn lớn.

#figure(
  image("../images/stability_comparison.png", width: 80%),
  caption: [So sánh condition number và solution error trên ma trận Hilbert]
) <fig:stability>

=== So sánh Hilbert và SPD: ý nghĩa về ổn định số học

Khi đặt kết quả của hai nhóm ma trận cạnh nhau, nhóm rút ra một nhận xét quan trọng: *độ ổn định của thuật toán không thể tách rời khỏi bản chất của dữ liệu đầu vào*. Trên ma trận SPD ngẫu nhiên, các phương pháp cho kết quả tốt và khá đồng đều. Trên ma trận Hilbert, sai số bị khuếch đại mạnh dù cùng một thuật toán vẫn được sử dụng.

Điều này cho thấy khi đánh giá chất lượng nghiệm trong thực tế, không nên chỉ quan sát một chỉ số duy nhất. Việc theo dõi đồng thời *condition number*, *relative residual* và *solution error* là cần thiết để tránh kết luận sai rằng bài toán đã được giải “tốt” chỉ vì residual nhỏ.

*(Chèn Bảng 1: So sánh condition number, relative residual và solution error giữa Hilbert và SPD)*

== Kết luận của phần thực nghiệm

Từ toàn bộ benchmark, nhóm nhận thấy không tồn tại một phương pháp tối ưu cho mọi loại dữ liệu.

- *Khử Gauss* và *LU* phù hợp khi cần nghiệm trực tiếp, ổn định và có thể kiểm soát tốt trên các ma trận khả nghịch thông thường.
- *LU* đặc biệt hữu ích khi cần giải lặp lại nhiều hệ với cùng ma trận hệ số nhưng khác vector \(b\).
- *Gauss-Seidel* phát huy ưu thế trên các ma trận có cấu trúc thuận lợi cho hội tụ, đặc biệt là ma trận chéo trội hoặc SPD, nơi chi phí thực tế có thể thấp hơn đáng kể so với các phương pháp trực tiếp.

Quan trọng hơn, kết quả thực nghiệm khẳng định rằng việc lựa chọn thuật toán trong tính toán khoa học không thể chỉ dựa vào công thức lý thuyết. Cần xét đồng thời đến *cấu trúc ma trận*, *độ ổn định số học* và *chi phí tính toán quan sát được từ thực nghiệm*. Đây cũng chính là ý nghĩa cốt lõi của Part 3: đưa các khái niệm như số điều kiện, residual và ổn định số ra khỏi lý thuyết thuần túy để đánh giá trên dữ liệu thực tế.