= Phụ lục

== Thiết lập benchmark

Tóm tắt cấu hình benchmark đã dùng trong Part 3 nhằm giúp việc đối chiếu số liệu được rõ ràng:

-  Thực nghiệm A sử dụng ma trận chéo trội nghiêm ngặt với các kích thước
  $n in {50, 100, 200, 500, 1000}$.
- Thực nghiệm B sử dụng hai lớp dữ liệu:
  + ma trận Hilbert với các kích thước $n in {3, 5, 8, 10, 12, 15}$,
  + ma trận SPD ngẫu nhiên với các kích thước $n in {5, 10, 20, 50, 100}$.
- Với mỗi bài toán, nghiệm chuẩn được chọn là
  $x_"true" = (1,1,dots,1)^T$
  và vế phải được dựng theo công thức
  $b = A x_"true"$.
- Mỗi thuật toán được chạy lặp lại nhiều lần để lấy thời gian thực thi trung bình.
- Các thước đo chính gồm: average runtime, relative residual error, solution error và condition number.

== Bảng số liệu benchmark

#figure(
  kind: table,
  table(
    columns: 4,
    align: (left, center, center, center),
    stroke: .4pt,
    inset: 6pt,

    table.header(
      [Kích thước $n$],
      [Gauss (giây)],
      [LU (giây)],
      [Gauss-Seidel (giây)],
    ),

    [50],   [0.00743397999995068], [0.007904059999964375], [0.005091100000026927],
    [100],  [0.054590980000011766], [0.05357215999993059], [0.01834283999996842],
    [200],  [0.41380258000008324], [0.38668693999989046], [0.06996342000002187],
    [500],  [6.588886739999907], [6.086413700000048], [0.4855199399999037],
    [1000], [66.86845896000004], [49.21678384000006], [2.1515959599999404],
  ),
  caption: [Thời gian thực thi trung bình của ba phương pháp theo kích thước $n$]
) <tbl:runtime-full>

#figure(
  kind: table,
  table(
    columns: 4,
    align: (left, center, center, center),
    stroke: .4pt,
    inset: 6pt,

    table.header(
      [Kích thước $n$],
      [Gauss: relative residual],
      [LU: relative residual],
      [Gauss-Seidel: relative residual],
    ),

    [50],   [2.57120764599466e-16], [1.7982476196557096e-16], [1.4728597399427674e-11],
    [100],  [3.9894949798543487e-16], [2.375493704813685e-16], [2.1043800620148006e-11],
    [200],  [6.294969635964853e-16], [3.61374988609456e-16], [2.240019006674828e-11],
    [500],  [8.5093836423896545e-16], [4.843538846929277e-16], [4.007728974872171e-12],
    [1000], [1.2150449245852734e-15], [7.142782504630557e-16], [4.117025142228604e-12],
  ),
  caption: [Sai số tương đối trên ma trận chéo trội theo kích thước $n$]
) <tbl:residual-full>

#text(size: 9pt, [
  #figure(
    kind: table,
    table(
      columns: 5,
      align: (left, center, center, center, center),
      stroke: .4pt,
      inset: 6pt,

      table.header(
        [$n$],
        [$kappa(H_n)$],
        [Gauss],
        [LU],
        [Gauss-Seidel],
      ),

      [3],  [524.0567775860644], [8.029504617323886e-15], [6.312995352117186e-16], [2.9409075559091467e-09],
      [5],  [476607.2502422687], [3.4933500817422506e-13], [4.0776002155697605e-13], [0.015614197644107443],
      [8],  [15257575538.072489], [3.585112236209358e-08], [1.2037318405713512e-07], [0.011843130706839124],
      [10], [16024413500363.82], [8.242288834150656e-05], [7.669642293005977e-05], [0.01863028911504514],
      [12], [1.760619121841585e+16], [0.24279706008136856], [0.21541779869276456], [0.019379423598475363],
      [15], [3.67568286586649e+17], [inf], [inf], [0.014763977682965666],
    ),
    caption: [Condition number và sai số nghiệm trên ma trận Hilbert]
  ) <tbl:hilbert-full>
])

#text(size: 9pt, [
  #figure(
    kind: table,
    table(
      columns: 5,
      align: (left, center, center, center, center),
      stroke: .4pt,
      inset: 6pt,

      table.header(
        [$n$],
        [$kappa(A)$],
        [Gauss],
        [LU],
        [Gauss-Seidel],
      ),

      [5],   [8.262747648772656], [3.8778423131653424e-16], [3.8778423131653424e-16], [3.186869297008191e-11],
      [10],  [26.66938769237467], [1.885092002791316e-15], [2.4351622812383723e-15], [9.63379670769499e-11],
      [20],  [101.65424472005893], [3.642394549208486e-15], [3.2267214558670763e-15], [1.8673990549723844e-10],
      [50],  [624.1109315740032], [2.8347292115470653e-14], [3.421524361122915e-14], [1.7073289801987625e-09],
      [100], [2494.188196919666], [1.3314414831191423e-13], [1.2874113401912214e-13], [0.05050155287436875],
    ),
    caption: [Condition number và sai số nghiệm trên ma trận SPD ngẫu nhiên]
  ) <tbl:spd-full>
])
