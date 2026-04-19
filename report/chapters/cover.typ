#let info-title(body) = text(weight: "semibold", 12pt, body)

#let member-row(name, id) = grid(
  columns: (1fr, 0.42fr),
  column-gutter: 0.28cm,
  align(left)[#name],
  align(right)[#id],
)

// first page
#align(center)[
  #text(16pt, weight: "bold")[TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM]

   #text(14pt, weight: "bold")[KHOA CÔNG NGHỆ THÔNG TIN]
  #v(1cm)
  #image("../images/logo.png", width: 30%)
  #v(1cm)
  #text(20pt, weight: "bold")[BÁO CÁO ĐỒ ÁN 1]
  #v(0.5cm)
  #text(22pt, weight: "bold")[Ma Trận và Cơ Sở của Tính Toán Khoa Học]
  #v(0.5cm)
  #text(14pt)[Môn học: Toán Ứng Dụng và Thống Kê]
  #v(1cm)
]

#align(center)[
  #block(width: 86%)[
    #line(length: 100%, stroke: 0.6pt + luma(160))
    #v(0.42cm)

    #grid(
      columns: (1.22fr, 0.92fr),
      column-gutter: 1.5cm,

      [
        #info-title[Thực hiện]
        #v(0.22cm)
        #text(10.6pt)[Nhóm 12 (Lớp C02024-3)]
        #v(0.18cm)

        #member-row([Nguyễn Ngọc Quang (NT)], [24120127])
        #v(0.10cm)
        #member-row([Đặng Quang Tiến], [24120149])
        #v(0.10cm)
        #member-row([Liên Trung Hiếu], [24120049])
        #v(0.10cm)
        #member-row([Trương Đình Nhật Huy], [24120064])
        #v(0.10cm)
        #member-row([Đinh Đức Hiếu], [24120002])
      ],

      [
        #info-title[Giảng viên hướng dẫn]
        #v(0.22cm)
        #text(10.6pt)[ThS. Võ Nam Thục Đoan]
        #v(0.14cm)
        #text(10.6pt)[ThS. Lê Nhựt Nam]
      ],
    )
  ]
]

#v(1fr)
#align(center)[
  TP. Hồ Chí Minh, ngày 20 tháng 4 năm 2026
]


