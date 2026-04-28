// code block
#let codeblock(lines) = block(
  width: 100%,
  fill: rgb("#F7F7F7"),
  stroke: 0.6pt + rgb("#D6D6D6"),
  inset: 10pt,
  radius: 4pt,
)[
  #set text(font: "Consolas", size: 9.5pt)
  #set par(justify: false, first-line-indent: 0em)

  #for (i, line) in lines.enumerate() [
    #grid(
      columns: (2em, 1fr),
      gutter: 0.8em,
      [
        #align(right)[
          #text(fill: rgb("#666666"))[#(i + 1)]
        ]
      ],
      [#line],
    )
  ]
]