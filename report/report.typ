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
  first-line-indent: (amount: 1.2em, all: true),
  leading: 0.72em,
)

#set list(indent: 1.5em)

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
#show heading.where(level: 1): it => [#text(fill: title-color, font: body-font, size: 20pt)[#it] #v(0.8em)]
#show heading.where(level: 1):  it => if true {pagebreak(weak: true);it} else {it}

// == phụ lục cấp 2
#show heading.where(level: 2): it => [
  #text(font: body-font, size: 16pt, fill: title-color,)[#it]
]

// === phụ lục cấp 3
#show heading.where(level: 3): it => [
  #text(font: body-font, fill: title-color,)[#it] #v(0.5em)
]
#show heading.where(level: 3): set heading(outlined: false)


// non-numbering
#show selector(<nonumber>): set heading(
  numbering: none,
  outlined: false,
)

// non-outlined
#show selector(<nooutlined>): set heading(
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
#include "chapters/cover.typ"
#include "chapters/group_work.typ"

// Mục lục
#outline(title: auto, depth: 3,indent: auto)

// header/footer
#show: chic.with(
  chic-header(
    left-side: [FIT-HCMUS],
    right-side: chic-heading-name(),
  ),
  chic-footer(
    right-side: chic-page-number(),
  ),
  chic-separator(1pt),
  chic-offset(14pt),
)

#include "chapters/intro.typ"
#include "chapters/part1_gauss.typ"
#include "chapters/part2_decomposition.typ"
#include "chapters/part3_solve_analysis.typ"
#include "chapters/conclude.typ"
#include "chapters/appendix.typ"