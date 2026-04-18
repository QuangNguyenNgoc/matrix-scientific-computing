# Báo Cáo Phân Tích Thực Nghiệm: Giải Hệ Phương Trình Tuyến Tính

## 1. Mục tiêu
Thực nghiệm này nhằm đánh giá và so sánh mức độ hiệu quả của 3 phương pháp giải hệ phương trình tuyến tính: **Khử Gauss (Partial Pivoting), Phân rã LU (Partial Pivoting) và lặp Gauss-Seidel**. Các phép thử được tiến hành để phân tích cụ thể trên 3 khía cạnh cốt lõi của tính toán khoa học:
- **Thời gian thực thi (Runtime)**: Quan sát thời gian chạy thực tế theo kích thước ma trận $n$, từ đó đối chiếu với độ phức tạp lý thuyết $\mathcal{O}(n^3)$ của phép khử chuẩn và $\mathcal{O}(kn^2)$ của phương pháp lặp.
- **Độ chính xác (Sai số)**: Đo lường mức độ khớp của nghiệm tính toán $x_{hat}$ qua sai số tương đối (Relative Residual: $\frac{||Ax_{hat} - b||_2}{||b||_2}$) và sai lệch nghiệm thực tế (Solution Error: $\frac{||x_{hat} - x_{true}||_2}{||x_{true}||_2}$).
- **Độ ổn định số học (Numerical Stability)**: Khảo sát hành vi của các phương pháp khi đối mặt với dữ liệu nhiễu/nhạy cảm (ma trận ill-conditioned) so với dữ liệu lý tưởng (well-conditioned).

## 2. Cách làm (Phương pháp luận)
Để đảm bảo kết quả phản ánh đúng bản chất "thuật toán ngoài thực tế", nhóm đã tiến hành theo quy trình sau:
- **Sinh dữ liệu kiểm thử**: 
  - *Thực nghiệm A (Đo thời gian/Hiệu năng):* Sinh các ma trận vuông chéo trội nghiêm ngặt (để đảm bảo Gauss-Seidel hội tụ) với kích thước tăng dần $n \in \{50, 100, 200, 500, 1000\}$.
  - *Thực nghiệm B (Ổn định số):* Sinh ra ma trận Hilbert đặc biệt xấu (ill-conditioned, số điều kiện $\kappa$ cực lớn) với cỡ nhỏ $n \in \{3, 5, 8, 10, 12, 15\}$, và một nhóm ma trận Đối xứng Xác định Dương (SPD) ngẫu nhiên (well-conditioned) với cỡ $n \in \{5, 10, 20, 50, 100\}$.
- **Cách thức thực thi**: Toàn bộ thuật toán được thực thi bằng mã nguồn **thuần túy (pure Python list)**, không dựa vào tối ưu C của thư viện (NumPy). Mỗi cỡ ma trận thực hiện chạy $5$ lần để lấy trung bình thời gian thực thi (Average Runtime). Vector $b$ được tạo ra bằng biểu thức $b = Ax_{true}$ với nghiệm chuẩn (ground truth) $x_{true}$ được gắn sẵn là vector toàn số 1 nhằm phục vụ việc tính toán sai số.
- **Thước đo**: Cả ba phương pháp sẽ được thu thập chỉ số runtime, relative residual error, solution error và lưu kết quả chi tiết thành dạng `.csv`.

## 3. Kết quả và nhận xét

Theo quá trình phân tích số liệu ghi nhận được từ hệ thống đo lường (benchmark), kết quả cho thấy những xu thế rất rõ rệt về hiệu năng cũng như giới hạn của từng phương pháp:

### 3.1. Phân tích về thời gian thực thi và chi phí tính toán
Theo kết quả đo từ thực nghiệm A, nhóm ghi nhận sự tăng trưởng chi phí tính toán rất khốc liệt đối với Gauss và LU. 
Với kích thước nhỏ ($n \le 100$), cả 3 thuật toán đều trả về kết quả trong thời gian ngắn (chỉ cỡ 0.00743397999995068 giây). Tuy nhiên, khi đẩy kích thước lên $n=1000$:
- **Khử Gauss và LU**: Thời gian chạy phình to lên mức 66.86845896000004 và 49.21678384000006 giây. Cả hai cho thấy độ trễ tăng xấp xỉ tỉ lệ thuận theo đúng chuẩn quy mô bậc 3 $\mathcal{O}(n^3)$. 
- **Gauss-Seidel**: Tỏ ra vượt trội hoàn toàn về tốc độ khi giải quyết ma trận kích thước cực lớn, tốn vỏn vẹn chỉ 2.1515959599999404 giây với khoảng 1000 vòng lặp. Việc ma trận nguồn được sinh theo chuẩn "chéo trội" giúp phương pháp lặp hội tụ cực kỳ nhanh, minh chứng rõ ràng cho lợi thế của lặp $\mathcal{O}(n^2)$ so với phương pháp tính đúng trong một số loại dữ liệu đặc thù.

*(Chừa chỗ: Chèn biểu đồ Đường (Line chart) Runtime so với kích thước $n$)*

### 3.2. Phân tích ổn định qua Ma trận nhiễu Hilbert vs Ma trận chuẩn (SPD)
Thông qua Thực nghiệm B, chúng tôi có đủ cơ sở để đánh giá điểm yếu chí mạng của toán học dẫu phân tích đúng theo công thức:

- **Đối với nhóm ma trận Random SPD (Well-conditioned):**
   Kết quả cho thấy số điều kiện (Condition Number, $\kappa$) khá nhỏ ($\kappa \approx$ 100). Tất cả các thuật toán bao gồm Gauss, LU và Gauss-Seidel duy trì độ chính xác cực tốt với mức sai số giải thuật (solution error) giữ vững ở ngưỡng máy tính: cỡ $\sim 10^{-15}$. Sự ổn định của các phương pháp giải hệ ở đây được cho là lý tưởng.

- **Trong trường hợp ma trận Hilbert (Ill-conditioned):**
   Khi tăng giá trị $n$ lên mức $n = 10, 12, 15$, số điều kiện của ma trận Hilbert bùng nổ lên cỡ $\sim 10^{15}$ đến $10^{18}$. Nhóm quan sát hiện tượng **mất mát chữ số có nghĩa** nghiêm trọng. Dù dùng kỹ thuật Partial Pivoting (chọn phần tử trội), cả hai thuật toán Gauss và LU đều bị nhiễu do sai số làm tròn tích luỹ (round-off error), khiến solution error ($||x - x_{true}||$) nhảy vọt, dù residual ($Ax - b$) tính ra vẫn có vẻ nhỏ đi chăng nữa. Nghĩa là máy tính có thể báo đã tìm ra sai số nhỏ, nhưng giá trị nghiệm thu về hoàn toàn trật chìa. Nhóm thu được Solution Error lên tới 1.303847564706011e-07 đối với $n=15$.
   Riêng đối với Gauss-Seidel, đây là ma trận xấu không đảm bảo chéo trội/SPD mạnh, hệ thống ghi nhận máy phải lặp hết hạn mức tối đa (max_iter = 5000) mà vẫn chưa thể hội tụ, đưa ra cấu trúc sai số tệ.

*(Chừa chỗ: Chèn bảng so sánh sai số giữa n nhỏ và n lớn với ma trận Hilbert)*

### Ý nghĩa tổng kết
Từ phân tích này cho thấy không có thuật toán nào là tuyệt đối cho mọi cấu trúc bài toán:
- Nên ưu tiên Gauss hoặc LU cho ma trận vừa và nhỏ, nơi đòi hỏi có đáp án tính chính xác một lần, hoặc khi phân rã LU có thể mang ra giải lại nhiều lần cho các vector $b$ khác nhau để tối ưu chi phí.
- Chỉ định luôn dùng Gauss-Seidel hoặc các giải thuật lặp trong trường hợp đặc thù hệ phương trình cỡ khổng lồ thưa thớt, hay ma trận đảm bảo tính chéo trội dương.
- Tính ổn định cực kỳ nhạy cảm với bản chất của input gốc (condition number) chứ không chỉ riêng ở chính thuật toán. Việc tính toán nên đo kỹ số điều kiện (Condition Number) trước, thay vì nhắm mắt lao vào tính toán.
