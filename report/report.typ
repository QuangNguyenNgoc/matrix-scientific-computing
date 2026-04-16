// module
#import "@preview/chic-hdr:0.5.0":*
#import "@preview/equate:0.3.2":*

// constraint
#let title-color = rgb("#1E3778")
#let body-color = rgb("#111111")
#let soft-color = rgb("#666666")

#let body-font = "Times New Roman"
#let mono-font = "Consolas"

// page + text + paragraph
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
)

#set text(
  font: body-font,
  size: 11.5pt,
  fill: body-color,
  lang: "vi",
)

#set par(
  justify: true,
  first-line-indent: 1.2em,
  leading: 0.72em,
)

// numbering
#set heading(
   numbering: (..nums) => {
    let s = nums.pos().map(str).join(".")
    if nums.pos().len() == 1 {
      // Style cho Level 1 (Số | Tiêu đề)
      return [
        #s #h(0.1em)
        #box(width: 1.2pt, height: 1em, fill: title-color.darken(30%), baseline: 15%)
        #h(0.1em)
      ]
    } else {
      // Style cho Level 2, 3 (Số.)
      return [#s.]
    }
  }
)

// = phần chính
#show heading.where(level: 1): it => [#text(fill: title-color, font: body-font, size: 22pt)[#it] #v(0.8em)]
#show heading.where(level: 1):  it => if true {pagebreak(weak: true);it} else {it}

// == phụ lục cấp 2
#show heading.where(level: 2): it => [
  #text(font: body-font, size: 16pt, fill: title-color,)[#it]
]

// === phụ lục cấp 3
#show heading.where(level: 3): it => [
  #text(font: body-font, fill: title-color,)[#it] #v(0.5em)
]

// non-numbering
#show selector(<nonumber>): set heading(
  numbering: none,
  outlined: false,
)

// math
#set math.equation(numbering: "(1.1)")
#show: equate.with(breakable: true, sub-numbering: true)

// figure caption
#show figure.caption: it => [
  #set text(size: 10pt, fill: soft-color)
  #strong[#it.supplement ~ #it.counter.display(it.numbering)]
  #it.separator
  #it.body
]

#show figure.where(kind: table): set figure.caption(position: top)

// table
#show table.cell: set par(
  justify: false,
  first-line-indent: 0em,
)

// code block
#let codeblock(lines) = block(
  width: 100%,
  fill: rgb("#F7F7F7"),
  stroke: 0.6pt + rgb("#D6D6D6"),
  inset: 10pt,
  radius: 4pt,
)[
  #set text(font: mono-font, size: 9.5pt)
  #set par(justify: false, first-line-indent: 0em)

  #for (i, line) in lines.enumerate() [
    #grid(
      columns: (2em, 1fr),
      gutter: 0.8em,
      [
        #align(right)[
          #text(fill: soft-color)[#(i + 1)]
        ]
      ],
      [#line],
    )
  ]
]

//// end of config

// first page
#align(center)[
  #text(16pt, weight: "bold")[TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN]\
  KHOA CÔNG NGHỆ THÔNG TIN
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

#v(1fr)
#align(center)[
  TP. Hồ Chí Minh, ngày 20 tháng 4 năm 2026
]
#pagebreak()

// Mục lục
#outline(title: auto, depth: 3,indent: auto)

#pagebreak()

// header/footer
#show: chic.with(
  chic-header(
    left-side: [Tên tài liệu],
    right-side: chic-heading-name(),
  ),
  chic-footer(
    right-side: chic-page-number(),
  ),
  chic-separator(1pt),
  chic-offset(14pt),
)

#include "modules/chapters/intro.typ"

= Đồ án 1 - Ma trận

== Giới thiệu
=== Motif
Đây là báo cáo viết bằng Typst.
Nội dung này đang cần bố sung. 
== Công thức

$ A x = b $

== Ma trận

$ mat(
  1, 2;
  3, 4
) $

#codeblock((
  "Group_<ID>/",
  "|-- README.md",
  "|-- requirements.txt",
  "|-- report/",
  "|   |-- report.pdf",
  "|   `-- report.tex",
))

 $ alpha = 5 x x /7  oo > integral_oo^oo  dif x   = -> => >= integral_a^x  oo sum_a_i angle.l alpha|x|a_i angle.r  dif x  $ <eq1>

 $ E &= m c^2 \
    &= sqrt(p^2 c^2 + m^2 c^4) $
