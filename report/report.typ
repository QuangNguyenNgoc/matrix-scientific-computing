#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
)

#set text(
  font: "Times New Roman",
  size: 12.5pt,
)

#set heading(
  numbering: "1.",
)

#align(center)[
  #text(14pt, weight: "bold")[TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN]  
  
  #text(13pt)[KHOA CÔNG NGHỆ THÔNG TIN]
  #v(2.5cm)
  #text(16pt, weight: "bold")[BÁO CÁO ĐỒ ÁN 1]
  #v(0.5cm)
  #text(22pt, weight: "bold")[Ma Trận và Cơ Sở của Tính Toán Khoa Học]
  #v(1cm)
  #text(14pt)[Môn học: Toán Ứng Dụng và Thống Kê]

  #v(2cm)
]

#align(left)[
  *Thành viên thực hiện:*  
  - Nguyễn Ngọc Quang --- MSSV: 24120127
  - Đặng Quang Tiến --- MSSV: 24120149
  - Liên Trung Hiếu --- MSSV: 24120049
  - Trương Đình Nhật Huy --- MSSV: 24120064 
  - Đinh Đức Hiếu --- MSSV: 24120002

  #v(0.8cm)

  *Giảng viên hướng dẫn:*  
  - ThS. Võ Nam Thục Đoan  
  - ThS. Lê Nhựt Nam  
]

#v(5cm)

#align(center)[
  TP. Hồ Chí Minh, ngày 20 tháng 4 năm 2026
]

#pagebreak()

#outline(title: [Mục lục])

#pagebreak()

#let intro() = [
= Giới thiệu đồ án

Đồ án này tập trung vào ba nhóm nội dung chính: phép khử Gauss và các ứng dụng, phân rã ma trận kết hợp trực quan hóa, và phân tích hiệu năng cũng như tính ổn định số. Mục tiêu không chỉ là cài đặt thuật toán từ đầu bằng Python mà còn phải hiểu rõ bản chất toán học, kiểm chứng kết quả và trình bày lại bằng báo cáo cùng video minh họa.

Trong quá trình thực hiện, nhóm thống nhất sử dụng Python làm ngôn ngữ chính, kết hợp với các thư viện hỗ trợ để kiểm chứng, trực quan hóa và phân tích kết quả. Phần cài đặt thuật toán được viết theo hướng tự xây dựng lại từ đầu, còn các thư viện như NumPy hoặc SciPy chỉ được dùng cho mục đích đối chiếu và kiểm chứng.

Báo cáo được tổ chức thành ba phần tương ứng với yêu cầu của đề bài. Phần đầu trình bày phép khử Gauss và các ứng dụng trực tiếp. Phần hai tập trung vào phân rã ma trận, chéo hóa và video Manim. Phần ba trình bày thực nghiệm benchmark, phân tích sai số và đánh giá tính ổn định số.
]

#intro()


= Đồ án 1 - Ma trận

== Giới thiệu

Đây là báo cáo viết bằng Typst.

== Công thức

$ A x = b $

== Ma trận

$ mat(
  1, 2;
  3, 4
) $


