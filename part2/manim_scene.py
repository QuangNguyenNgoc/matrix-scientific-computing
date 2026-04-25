from manim import *
import unicodedata
import numpy as np

from decomposition import svdDecomp
from diagonalization import diagonalize, matrixMultiply, matrixTranspose


FONT = "Times New Roman"
VIET_TEX_TEMPLATE = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=rf"""
\usepackage{{fontspec}}
\usepackage[vietnamese]{{babel}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{ragged2e}}
\IfFontExistsTF{{{FONT}}}{{
    \setmainfont{{{FONT}}}
    \setsansfont{{{FONT}}}
}}{{
    \setmainfont{{TeX Gyre Termes}}
    \setsansfont{{TeX Gyre Termes}}
}}
""",
)
DIAG_MATRIX = [[4.0, 1.0], [2.0, 3.0]]
SVD_MATRIX = [[2.0, 1.0], [1.0, 2.0]]
ANIMATION_SCALE = 1.45
WAIT_SCALE = 2.35


def latex_text(text):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    text = unicodedata.normalize("NFC", text)
    return "".join(replacements.get(char, char) for char in text)


def tex_num(value):
    value = 0.0 if abs(float(value)) < 1e-9 else float(value)
    known = [
        (1 / np.sqrt(2), r"\frac1{\sqrt2}"),
        (-1 / np.sqrt(2), r"-\frac1{\sqrt2}"),
        (3 / np.sqrt(2), r"\frac3{\sqrt2}"),
        (-3 / np.sqrt(2), r"-\frac3{\sqrt2}"),
        (1 / np.sqrt(5), r"\frac1{\sqrt5}"),
        (-1 / np.sqrt(5), r"-\frac1{\sqrt5}"),
        (2 / np.sqrt(5), r"\frac2{\sqrt5}"),
        (-2 / np.sqrt(5), r"-\frac2{\sqrt5}"),
        (np.sqrt(2) / 3, r"\frac{\sqrt2}{3}"),
        (-np.sqrt(2) / 3, r"-\frac{\sqrt2}{3}"),
        (2 * np.sqrt(2) / 3, r"\frac{2\sqrt2}{3}"),
        (-2 * np.sqrt(2) / 3, r"-\frac{2\sqrt2}{3}"),
        (np.sqrt(5) / 3, r"\frac{\sqrt5}{3}"),
        (-np.sqrt(5) / 3, r"-\frac{\sqrt5}{3}"),
    ]
    for target, text in known:
        if abs(value - target) < 1e-6:
            return text
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def text_num(value):
    value = 0.0 if abs(float(value)) < 1e-9 else float(value)
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def tex_matrix(matrix):
    rows = ["&".join(tex_num(value) for value in row) for row in matrix]
    return r"\begin{pmatrix}" + r"\\".join(rows) + r"\end{pmatrix}"


def tex_column(vector):
    return tex_matrix([[value] for value in vector])


def get_col(matrix, index):
    return [row[index] for row in matrix]


def sub_lambda(matrix, value):
    return [
        [matrix[row][col] - (value if row == col else 0.0) for col in range(len(matrix))]
        for row in range(len(matrix))
    ]


def scaled_vec(vector, scale=2.0):
    return (np.array(vector, dtype=float) * scale).tolist()


class Part2StoryboardMathTex(MovingCameraScene):
    def play(self, *animations, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * ANIMATION_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1, *args, **kwargs):
        return super().wait(duration * WAIT_SCALE, *args, **kwargs)

    def construct(self):
        self.camera.background_color = "#101318"
        self.diag_matrix = DIAG_MATRIX
        self.diag_p, self.diag_d, self.diag_p_inv = diagonalize(self.diag_matrix)
        self.diag_eigs = [self.diag_d[i][i] for i in range(len(self.diag_d))]

        self.svd_matrix = SVD_MATRIX
        self.svd_u, self.svd_sigma, self.svd_vt = svdDecomp(self.svd_matrix)
        self.svd_v = matrixTranspose(self.svd_vt)
        self.svd_ata = matrixMultiply(matrixTranspose(self.svd_matrix), self.svd_matrix)
        self.svd_lambdas = [self.svd_sigma[i][i] ** 2 for i in range(len(self.svd_sigma))]

        self.scene_01_opening()
        self.scene_02_scope()
        self.scene_03_diag_example()
        self.scene_04_diag_eigenvalues()
        self.scene_05_diag_vector_lambda_5()
        self.scene_06_diag_vector_lambda_2()
        self.scene_07_diag_factors()
        self.scene_08_diag_result()
        self.scene_08_diag_geometry()
        self.scene_09_to_svd()
        self.scene_10_svd_example()
        self.scene_11_svd_ata()
        self.scene_12_svd_eigenvalues()
        self.scene_13_svd_vectors()
        self.scene_14_svd_sigma_u()
        self.scene_15_svd_final()
        self.scene_16_svd_geometry()

    def VText(self, text, size=28, color=WHITE, weight=NORMAL):
        prefix = r"\rmfamily\bfseries " if weight == BOLD else r"\rmfamily "
        return Tex(
            prefix + latex_text(text),
            tex_template=VIET_TEX_TEMPLATE,
            font_size=size,
            color=color,
        )

    def VParagraph(self, text, size=25, color=WHITE, width_cm=6.4):
        body = latex_text(" ".join(text.split()))
        return Tex(
            rf"\begin{{minipage}}{{{width_cm}cm}}\justifying\setlength{{\parindent}}{{0pt}}\emergencystretch=2em\rmfamily {body}\end{{minipage}}",
            tex_template=VIET_TEX_TEMPLATE,
            font_size=size,
            color=color,
        )

    def Title(self, text, color=BLUE):
        return self.VText(text, 38, color, BOLD).to_edge(UP)

    def Explain(self, text, color=GRAY_A):
        return self.VText(text, 24, color).to_edge(DOWN)

    def fit(self, mob, max_width=6.0, max_height=None):
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if max_height is not None and mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def left_col(self, mob, y=0.15, max_width=5.9):
        self.fit(mob, max_width)
        return mob.move_to(LEFT * 3.35 + UP * y)

    def right_col(self, mob, y=0.15, max_width=5.9):
        self.fit(mob, max_width)
        return mob.move_to(RIGHT * 3.35 + UP * y)

    def center_content(self, mob, y=0.25, max_width=11.4, max_height=None):
        self.fit(mob, max_width, max_height)
        return mob.move_to(UP * y)

    def underline(self, mob, color=YELLOW):
        line = Line(mob.get_left(), mob.get_right(), color=color, stroke_width=3)
        line.next_to(mob, DOWN, buff=0.08)
        return line

    def wipe(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

    def write_sequence(self, items, wait=0.35, run_time=0.8):
        for item in items:
            self.play(Write(item), run_time=run_time)
            self.wait(wait)

    def equation_flow(self, title, equations, result_tex, explain, result_color=YELLOW, highlights=None):
        current = self.center_content(MathTex(equations[0]).scale(0.84), y=0.85, max_width=10.6)
        faded = None
        arrow = None

        self.play(FadeIn(title), Write(current), run_time=1.0)
        for tex in equations[1:]:
            next_line = self.center_content(MathTex(tex).scale(0.84), y=0.0, max_width=10.6)
            next_arrow = MathTex(r"\Downarrow", color=GRAY_A).scale(0.5).move_to(UP * 0.45)
            animations = [
                current.animate.scale(0.82).move_to(UP * 1.38).set_color(GRAY_B),
                FadeIn(next_arrow, shift=DOWN * 0.08),
                FadeIn(next_line, shift=DOWN * 0.14),
            ]
            if faded is not None:
                animations.append(FadeOut(faded, shift=UP * 0.12))
            if arrow is not None:
                animations.append(FadeOut(arrow, shift=UP * 0.12))

            self.play(*animations, run_time=1.05)
            self.play(Indicate(next_line, color=result_color), run_time=0.35)
            self.wait(0.35)
            faded = current
            arrow = next_arrow
            current = next_line

        result = MathTex(result_tex, color=result_color).scale(0.9)
        result.next_to(current, DOWN, buff=0.62)
        self.fit(result, max_width=10.2)
        underline = self.underline(result, result_color)
        fade_old = []
        if faded is not None:
            fade_old.append(FadeOut(faded, shift=UP * 0.1))
        if arrow is not None:
            fade_old.append(FadeOut(arrow, shift=UP * 0.1))

        self.play(*fade_old, Write(result), Create(underline), FadeIn(explain), run_time=1.0)
        for term in highlights or []:
            self.play(Indicate(result.get_part_by_tex(term), color=result_color), run_time=0.8)
        return VGroup(current, result, underline, explain)

    def axes_small(self):
        return NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.2,
            y_length=4.2,
            background_line_style={"stroke_opacity": 0.28, "stroke_width": 1},
            axis_config={"stroke_color": GRAY_B, "stroke_width": 2},
        )

    def arrow_vec(self, axes, vector, color, label=None):
        arrow = Arrow(
            axes.c2p(0, 0),
            axes.c2p(float(vector[0]), float(vector[1])),
            buff=0,
            color=color,
            stroke_width=6,
        )
        if label is None:
            return arrow
        text = MathTex(label, color=color).scale(0.72).next_to(arrow.get_end(), UR, buff=0.08)
        return VGroup(arrow, text)

    def scene_01_opening(self):
        title = self.VText("Phân rã ma trận và chéo hóa", 44, WHITE, BOLD)
        group = self.VText("Nhóm 12 - 24CTT3 - HCMUS", 28, BLUE).next_to(title, DOWN, buff=0.45)
        course = self.VText("Môn Toán Ứng Dụng và Thống Kê", 24, GRAY_A).next_to(group, DOWN, buff=0.25)
        tagline = self.VText("Từ trị riêng, vector riêng đến SVD và ý nghĩa hình học", 23, YELLOW).to_edge(DOWN)

        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(group, shift=UP * 0.25), run_time=1.0)
        self.play(FadeIn(course, shift=UP * 0.15), run_time=1.0)
        self.play(FadeIn(tagline), run_time=0.8)
        self.wait(2)
        self.play(title.animate.scale(0.58).to_edge(UP), FadeOut(group), FadeOut(course), FadeOut(tagline), run_time=1.0)
        self.play(FadeOut(title), run_time=0.4)

    def scene_02_scope(self):
        title = self.Title("Chéo hóa ma trận", BLUE)
        formula = MathTex(r"A=PDP^{-1}", color=YELLOW).scale(1.0)
        lines = VGroup(
            self.VParagraph(
                "Chéo hóa biểu diễn một ma trận vuông A bằng công thức bên trên; trong đó D là ma trận "
                "đường chéo chứa các trị riêng. Các cột của P là những vector riêng tương ứng.",
                25,
                WHITE,
            ),
            self.VParagraph(
                "Khi chuyển sang eigenbasis, phép biến đổi chỉ còn co giãn theo từng trục riêng.",
                25,
                BLUE,
            ),
            self.VParagraph(
                "Nhờ vậy ta tính lũy thừa ma trận và hiểu hình học của A dễ hơn.",
                25,
                GRAY_A,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        self.left_col(lines, y=-0.35, max_width=5.95)

        axes = self.axes_small().scale(0.85).move_to(RIGHT * 3.35 + DOWN * 0.2)
        v1 = self.arrow_vec(axes, [1.6, 1.1], BLUE, r"v_1")
        v2 = self.arrow_vec(axes, [-0.8, 1.45], TEAL, r"v_2")
        lambda_v1 = self.arrow_vec(axes, [2.45, 1.68], YELLOW, r"\lambda_1v_1")
        lambda_v2 = self.arrow_vec(axes, [-1.15, 2.08], ORANGE, r"\lambda_2v_2")
        eigen_note = VGroup(
            MathTex(r"Av_i=\lambda_i v_i", color=YELLOW).scale(0.5),
            self.VText("A chỉ kéo giãn trên hướng riêng", 22, GRAY_A),
        ).arrange(DOWN, buff=0.16).next_to(axes, DOWN, buff=0.18)
        visual = VGroup(axes, v1, v2, lambda_v1, lambda_v2, eigen_note)

        self.play(FadeIn(title), run_time=0.8)
        self.play(Write(formula), run_time=0.8)
        self.play(formula.animate.scale(0.78).move_to(LEFT * 3.35 + UP * 1.75), run_time=0.8, rate_func=smooth)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.06) for line in lines], lag_ratio=0.13), run_time=1.55)
        self.play(Create(axes), GrowArrow(v1[0]), FadeIn(v1[1]), GrowArrow(v2[0]), FadeIn(v2[1]), run_time=1.1)
        self.play(
            TransformFromCopy(v1[0], lambda_v1[0]),
            FadeIn(lambda_v1[1]),
            TransformFromCopy(v2[0], lambda_v2[0]),
            FadeIn(lambda_v2[1]),
            FadeIn(eigen_note, shift=UP * 0.1),
            run_time=1.2,
        )
        self.play(
            Indicate(formula.get_part_by_tex("D"), color=YELLOW),
            Indicate(visual, color=BLUE),
            run_time=0.6,
        )
        self.wait(0.45)
        self.wipe()

    def scene_03_diag_example(self):
        title = self.Title("Ví dụ chéo hóa", BLUE)
        matrix = MathTex(r"A=" + tex_matrix(self.diag_matrix)).scale(1.05)
        formula = MathTex(r"A=PDP^{-1}").scale(0.92).next_to(matrix, DOWN, buff=0.8)
        formula.set_color_by_tex("P", BLUE)
        formula.set_color_by_tex("D", YELLOW)
        formula.set_color_by_tex("P^{-1}", GREEN)
        self.center_content(VGroup(matrix, formula), y=0.05, max_width=7.2)
        explain = VGroup(
            self.VText("Mục tiêu: tìm", 24, GRAY_A),
            MathTex(r"P,\ D,\ P^{-1}", color=YELLOW).scale(0.52),
            self.VText("để đưa A về dạng đường chéo.", 24, GRAY_A),
        ).arrange(RIGHT, buff=0.16).to_edge(DOWN)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(matrix, shift=DOWN * 0.4), run_time=1.2)
        self.play(Write(formula), FadeIn(explain), run_time=1.1)
        self.wait(3)
        self.wipe()

    def scene_04_diag_eigenvalues(self):
        title = self.Title("Tìm trị riêng của A", BLUE)
        explain = self.Explain("Hai trị riêng phân biệt là điều kiện đủ để chéo hóa được.")
        a, b = self.diag_matrix[0]
        c, d = self.diag_matrix[1]
        trace = a + d
        det = a * d - b * c
        ev1, ev2 = self.diag_eigs
        equations = [
            r"\det(A-\lambda I)=0",
            rf"\det\begin{{pmatrix}}{tex_num(a)}-\lambda&{tex_num(b)}\\{tex_num(c)}&{tex_num(d)}-\lambda\end{{pmatrix}}=0",
            rf"({tex_num(a)}-\lambda)({tex_num(d)}-\lambda)-{tex_num(b * c)}=0",
            rf"\lambda^2-{tex_num(trace)}\lambda+{tex_num(det)}=0",
            rf"(\lambda-{tex_num(ev1)})(\lambda-{tex_num(ev2)})=0",
        ]

        self.equation_flow(
            title,
            equations,
            rf"\lambda_1={tex_num(ev1)},\qquad \lambda_2={tex_num(ev2)}",
            explain,
            YELLOW,
            highlights=[tex_num(ev1), tex_num(ev2)],
        )
        self.wait(2.5)
        self.wipe()

    def scene_05_diag_vector_lambda_5(self):
        ev = self.diag_eigs[0]
        vector = get_col(self.diag_p, 0)
        title = self.Title(f"Vector riêng ứng với λ₁ = {text_num(ev)}", BLUE)
        left_steps = VGroup(
            MathTex(rf"(A-{tex_num(ev)}I)x=0"),
            MathTex(tex_matrix(sub_lambda(self.diag_matrix, ev)) + r"\begin{pmatrix}x_1\\x_2\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}"),
            MathTex(r"-x_1+x_2=0\Rightarrow x_1=x_2"),
            MathTex(r"v_1=" + tex_column(vector), color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.78)
        self.left_col(left_steps, y=0.25, max_width=6.1)
        axes = self.right_col(self.axes_small(), y=-0.05, max_width=4.6)
        v1 = self.arrow_vec(axes, scaled_vec(vector, 2.1), GREEN, r"v_1")

        self.play(FadeIn(title), Create(axes), run_time=1.0)
        self.write_sequence(left_steps[:3], wait=0.4)
        self.play(Write(left_steps[3]), run_time=1.0)
        self.play(GrowArrow(v1[0]), FadeIn(v1[1]), run_time=1.0)
        self.play(Circumscribe(left_steps[3], color=GREEN), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_06_diag_vector_lambda_2(self):
        ev = self.diag_eigs[1]
        vector = get_col(self.diag_p, 1)
        title = self.Title(f"Vector riêng ứng với λ₂ = {text_num(ev)}", BLUE)
        left_steps = VGroup(
            MathTex(rf"(A-{tex_num(ev)}I)x=0"),
            MathTex(tex_matrix(sub_lambda(self.diag_matrix, ev)) + r"\begin{pmatrix}x_1\\x_2\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}"),
            MathTex(r"2x_1+x_2=0\Rightarrow x_2=-2x_1"),
            MathTex(r"v_2=" + tex_column(vector), color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.78)
        self.left_col(left_steps, y=0.25, max_width=6.1)
        axes = self.right_col(self.axes_small(), y=-0.05, max_width=4.6)
        v1 = self.arrow_vec(axes, scaled_vec(get_col(self.diag_p, 0), 2.1), GREEN, r"v_1").set_opacity(0.35)
        v2 = self.arrow_vec(axes, scaled_vec(vector, 2.1), ORANGE, r"v_2")
        note = VGroup(
            MathTex(r"v_1,\ v_2", color=YELLOW).scale(0.52),
            self.VText("độc lập tuyến tính", 26, YELLOW),
        ).arrange(RIGHT, buff=0.14).to_edge(DOWN)

        self.play(FadeIn(title), Create(axes), FadeIn(v1), run_time=1.0)
        self.write_sequence(left_steps[:3], wait=0.4)
        self.play(Write(left_steps[3]), GrowArrow(v2[0]), FadeIn(v2[1]), run_time=1.0)
        self.play(FadeIn(note), Circumscribe(left_steps[3], color=ORANGE), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_07_diag_factors(self):
        title = VGroup(
            self.VText("Dựng", 38, BLUE, BOLD),
            MathTex(r"P,\ D,\ P^{-1}", color=BLUE).scale(0.78),
        ).arrange(RIGHT, buff=0.22).to_edge(UP)
        axes = self.right_col(self.axes_small(), y=-0.05, max_width=4.6)
        ev1, ev2 = self.diag_eigs
        v1 = self.arrow_vec(axes, scaled_vec(get_col(self.diag_p, 0), 2.1), GREEN, r"v_1")
        v2 = self.arrow_vec(axes, scaled_vec(get_col(self.diag_p, 1), 2.1), ORANGE, r"v_2")
        p = MathTex(r"P=" + tex_matrix(self.diag_p), color=BLUE).scale(0.78)
        d = MathTex(r"D=" + tex_matrix(self.diag_d), color=YELLOW).scale(0.78)
        pinv = MathTex(r"P^{-1}=" + tex_matrix(self.diag_p_inv), color=GREEN).scale(0.72)
        left = self.left_col(VGroup(p, d, pinv).arrange(DOWN, aligned_edge=LEFT, buff=0.45), y=0.1, max_width=6.0)
        formula = MathTex(r"A=PDP^{-1}", color=WHITE).scale(0.9).to_edge(DOWN)

        self.play(FadeIn(title), Create(axes), FadeIn(v1), FadeIn(v2), run_time=1.0)
        self.play(TransformFromCopy(v1, p), TransformFromCopy(v2, p), run_time=1.2)
        self.play(Write(d), run_time=0.9)
        self.play(Indicate(d.get_part_by_tex(tex_num(ev1)), color=YELLOW), Indicate(d.get_part_by_tex(tex_num(ev2)), color=YELLOW), run_time=0.9)
        self.play(Write(pinv), run_time=0.9)
        self.play(TransformFromCopy(left, formula), run_time=1.2)
        self.wait(3)
        self.wipe()

    def scene_08_diag_result(self):
        title = VGroup(
            self.VText("Kết quả chéo hóa của", 36, BLUE, BOLD),
            MathTex(r"A", color=YELLOW).scale(0.78),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        base = MathTex(r"A=", "P", "D", r"P^{-1}", color=WHITE).scale(1.0).move_to(UP * 1.35)
        base[1].set_color(BLUE)
        base[2].set_color(YELLOW)
        base[3].set_color(GREEN)

        p = MathTex(r"P=" + tex_matrix(self.diag_p), color=BLUE).scale(0.72)
        d = MathTex(r"D=" + tex_matrix(self.diag_d), color=YELLOW).scale(0.72)
        pinv = MathTex(r"P^{-1}=" + tex_matrix(self.diag_p_inv), color=GREEN).scale(0.66)
        factors = VGroup(p, d, pinv).arrange(RIGHT, buff=0.45)
        self.center_content(factors, y=0.25, max_width=11.4)

        expanded = MathTex(
            tex_matrix(self.diag_matrix)
            + r"="
            + tex_matrix(self.diag_p)
            + tex_matrix(self.diag_d)
            + tex_matrix(self.diag_p_inv),
            color=WHITE,
        ).scale(0.55)
        self.center_content(expanded, y=-1.0, max_width=11.6)

        rebuilt = matrixMultiply(matrixMultiply(self.diag_p, self.diag_d), self.diag_p_inv)
        check = MathTex(
            r"PDP^{-1}=" + tex_matrix(rebuilt) + r"=A",
            color=YELLOW,
        ).scale(0.68).to_edge(DOWN)

        self.play(FadeIn(title), Write(base), run_time=1.0)
        self.play(
            LaggedStart(
                TransformFromCopy(base.get_part_by_tex("P"), p),
                TransformFromCopy(base.get_part_by_tex("D"), d),
                TransformFromCopy(base.get_part_by_tex("P^{-1}"), pinv),
                lag_ratio=0.18,
            ),
            run_time=1.5,
        )
        self.play(Indicate(p, color=BLUE), Indicate(d, color=YELLOW), Indicate(pinv, color=GREEN), run_time=1.0)
        self.play(ReplacementTransform(VGroup(base, factors), expanded), run_time=1.4)
        self.play(Circumscribe(expanded, color=YELLOW), run_time=1.0)
        self.play(TransformFromCopy(expanded, check), run_time=1.1)
        self.play(Indicate(check.get_part_by_tex("A"), color=YELLOW), run_time=0.8)
        self.wait(2.5)
        self.wipe()

    def scene_08_diag_geometry(self):
        title = self.Title("Ý nghĩa hình học của chéo hóa", BLUE)
        axes = self.right_col(self.axes_small().scale(1.15), y=-0.05, max_width=4.9)
        square = Polygon(axes.c2p(0, 0), axes.c2p(1, 0), axes.c2p(1, 1), axes.c2p(0, 1), color=GRAY_A)
        x_demo = [0.45, 0.25]
        bx_demo = [row[0] * x_demo[0] + row[1] * x_demo[1] for row in self.diag_matrix]
        x_vec = self.arrow_vec(axes, x_demo, YELLOW, r"x")
        v1 = self.arrow_vec(axes, scaled_vec(get_col(self.diag_p, 0), 1.9), GREEN, r"v_1")
        v2 = self.arrow_vec(axes, scaled_vec(get_col(self.diag_p, 1), 1.9), ORANGE, r"v_2")
        labels = VGroup(
            MathTex(r"P^{-1}:\ \text{change basis}").scale(0.58),
            MathTex(r"D:\ \text{scale}").scale(0.58),
            MathTex(r"P:\ \text{return}").scale(0.58),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.left_col(labels, y=0.75, max_width=5.8)
        explain = self.Explain("Đổi cơ sở -> co giãn theo trị riêng -> quay về hệ chuẩn.")
        bx = self.arrow_vec(axes, bx_demo, RED, r"Ax")

        self.play(FadeIn(title), Create(axes), Create(square), FadeIn(v1), FadeIn(v2), GrowArrow(x_vec[0]), FadeIn(x_vec[1]), run_time=1.5)
        self.play(Write(labels[0]), FadeIn(explain), run_time=0.8)
        self.play(Indicate(x_vec, color=YELLOW), run_time=0.9)
        self.play(Write(labels[1]), run_time=0.8)
        self.play(v1.animate.set_opacity(1), v2.animate.set_opacity(1), square.animate.stretch(1.45, 0).stretch(0.9, 1), run_time=1.2)
        self.play(Write(labels[2]), run_time=0.8)
        self.play(TransformFromCopy(x_vec, bx), run_time=1.0)
        self.wait(2.7)
        self.wipe()

    def scene_09_to_svd(self):
        title = self.Title("Phân rã SVD", TEAL)
        formula = MathTex(r"B=U\Sigma V^T", color=YELLOW).scale(0.92)
        lines = VGroup(
            self.VParagraph(
                "Phân rã SVD biểu diễn ma trận B bằng công thức bên trên; trong đó U và V là các ma trận "
                "trực giao, còn Σ là ma trận đường chéo chứa các singular values.",
                24,
                WHITE,
            ),
            self.VParagraph(
                "Về mặt hình học, SVD mô tả phép biến đổi tuyến tính thành ba bước rất trực quan: "
                "xoay hệ tọa độ, co giãn theo các trục chính, rồi xoay lần nữa.",
                24,
                TEAL,
            ),
            self.VParagraph(
                "Đây là công cụ quan trọng vì ổn định số học, giúp phân tích cấu trúc ma trận, "
                "nén dữ liệu, xấp xỉ hạng thấp và nhiều ứng dụng trong tính toán khoa học.",
                24,
                GRAY_A,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.left_col(lines, y=-0.35, max_width=6.0)

        mini_axes = NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.0, 2.0, 1],
            x_length=4.5,
            y_length=3.6,
            background_line_style={"stroke_opacity": 0.18, "stroke_width": 1},
            axis_config={"stroke_color": GRAY_B, "stroke_width": 2},
        ).move_to(RIGHT * 3.35 + DOWN * 0.15)
        circle = Circle(radius=0.72, color=WHITE, stroke_width=4).move_to(mini_axes.c2p(0, 0))
        rotated_circle = circle.copy().rotate(-PI / 4, about_point=mini_axes.c2p(0, 0)).set_color(BLUE)
        ellipse = Ellipse(width=3.25, height=1.05, color=YELLOW, stroke_width=5).move_to(mini_axes.c2p(0, 0)).rotate(-PI / 4)
        final_ellipse = ellipse.copy().rotate(PI / 4, about_point=mini_axes.c2p(0, 0)).set_color(RED)

        self.play(FadeIn(title), run_time=0.8)
        self.play(Write(formula), run_time=0.8)
        self.play(formula.animate.scale(0.76).move_to(LEFT * 3.35 + UP * 1.75), run_time=0.8, rate_func=smooth)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.05) for line in lines], lag_ratio=0.09), run_time=1.75)
        self.play(Create(mini_axes), Create(circle), run_time=0.9)
        self.play(Transform(circle, rotated_circle), run_time=0.9, rate_func=smooth)
        self.play(Transform(circle, ellipse), run_time=0.95, rate_func=smooth)
        self.play(Transform(circle, final_ellipse), run_time=0.95, rate_func=smooth)
        self.play(
            Indicate(formula.get_part_by_tex(r"\Sigma"), color=YELLOW),
            Indicate(circle, color=TEAL),
            run_time=0.65,
        )
        self.wait(0.45)
        self.wipe()

    def scene_10_svd_example(self):
        title = self.Title("Ví dụ phân rã ma trận SVD", TEAL)
        left = self.left_col(MathTex(r"B=" + tex_matrix(self.svd_matrix)).scale(1.05), y=0.6)
        right = self.right_col(MathTex(r"B=U\Sigma V^T", color=YELLOW).scale(0.98), y=0.6)
        explain = VGroup(
            self.VText("Theo code:", 24, GRAY_A),
            MathTex(r"B^T B", color=GRAY_A).scale(0.5),
            self.VText("-> trị riêng -> singular values -> V -> U", 24, GRAY_A),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(left, shift=DOWN * 0.25), Write(right), FadeIn(explain), run_time=1.2)
        self.wait(3)
        self.wipe()

    def scene_11_svd_ata(self):
        title = VGroup(
            self.VText("Tính", 38, TEAL, BOLD),
            MathTex(r"B^T B", color=TEAL).scale(0.78),
            self.VText("từng ô", 38, TEAL, BOLD),
        ).arrange(RIGHT, buff=0.18).to_edge(UP)
        at = matrixTranspose(self.svd_matrix)
        left = self.left_col(MathTex(r"B^T B=" + tex_matrix(at) + tex_matrix(self.svd_matrix)).scale(0.74), y=1.05, max_width=6.15)
        result = self.right_col(MathTex(r"B^T B=" + tex_matrix(self.svd_ata), color=YELLOW).scale(0.88), y=0.55)
        a11 = at[0][0] * self.svd_matrix[0][0] + at[0][1] * self.svd_matrix[1][0]
        a12 = at[0][0] * self.svd_matrix[0][1] + at[0][1] * self.svd_matrix[1][1]
        a21 = at[1][0] * self.svd_matrix[0][0] + at[1][1] * self.svd_matrix[1][0]
        a22 = at[1][0] * self.svd_matrix[0][1] + at[1][1] * self.svd_matrix[1][1]
        calcs = VGroup(
            MathTex(rf"{tex_num(at[0][0])}\cdot{tex_num(self.svd_matrix[0][0])}+{tex_num(at[0][1])}\cdot{tex_num(self.svd_matrix[1][0])}={tex_num(a11)}"),
            MathTex(rf"{tex_num(at[0][0])}\cdot{tex_num(self.svd_matrix[0][1])}+{tex_num(at[0][1])}\cdot{tex_num(self.svd_matrix[1][1])}={tex_num(a12)}"),
            MathTex(rf"{tex_num(at[1][0])}\cdot{tex_num(self.svd_matrix[0][0])}+{tex_num(at[1][1])}\cdot{tex_num(self.svd_matrix[1][0])}={tex_num(a21)}"),
            MathTex(rf"{tex_num(at[1][0])}\cdot{tex_num(self.svd_matrix[0][1])}+{tex_num(at[1][1])}\cdot{tex_num(self.svd_matrix[1][1])}={tex_num(a22)}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).scale(0.72)
        self.left_col(calcs, y=-1.0, max_width=6.0)
        explain = VGroup(
            self.VText("Mỗi ô của", 24, GRAY_A),
            MathTex(r"B^T B", color=GRAY_A).scale(0.5),
            self.VText("được tạo từ một tích vô hướng.", 24, GRAY_A),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN)

        self.play(FadeIn(title), Write(left), FadeIn(explain), run_time=1.1)
        for calc in calcs:
            self.play(Write(calc), run_time=0.75)
            self.play(Indicate(calc, color=YELLOW), run_time=0.4)
        self.play(FadeIn(result), Circumscribe(result, color=YELLOW), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_12_svd_eigenvalues(self):
        title = VGroup(
            self.VText("Trị riêng của", 38, TEAL, BOLD),
            MathTex(r"B^T B", color=TEAL).scale(0.78),
        ).arrange(RIGHT, buff=0.18).to_edge(UP)
        a, b = self.svd_ata[0]
        c, d = self.svd_ata[1]
        trace = a + d
        det = a * d - b * c
        ev1, ev2 = self.svd_lambdas
        sigma1, sigma2 = self.svd_sigma[0][0], self.svd_sigma[1][1]
        equations = [
            r"\det(B^T B-\lambda I)=0",
            rf"\det\begin{{pmatrix}}{tex_num(a)}-\lambda&{tex_num(b)}\\{tex_num(c)}&{tex_num(d)}-\lambda\end{{pmatrix}}=0",
            rf"({tex_num(a)}-\lambda)({tex_num(d)}-\lambda)-{tex_num(b * c)}=0",
            rf"\lambda^2-{tex_num(trace)}\lambda+{tex_num(det)}=0",
            rf"\lambda_1={tex_num(ev1)},\qquad\lambda_2={tex_num(ev2)}",
        ]
        explain = VGroup(
            self.VText("Singular values là căn bậc hai của trị riêng dương của", 24, GRAY_A),
            MathTex(r"B^T B", color=GRAY_A).scale(0.5),
        ).arrange(RIGHT, buff=0.12)
        self.fit(explain, max_width=11.2)
        explain.to_edge(DOWN)

        self.equation_flow(
            title,
            equations,
            rf"\sigma_1=\sqrt{{{tex_num(ev1)}}}={tex_num(sigma1)},\qquad \sigma_2=\sqrt{{{tex_num(ev2)}}}={tex_num(sigma2)}",
            explain,
            YELLOW,
            highlights=[tex_num(sigma1), tex_num(sigma2)],
        )
        self.wait(2.5)
        self.wipe()

    def scene_13_svd_vectors(self):
        title = self.Title("Vector riêng tạo nên V", TEAL)
        ev1, ev2 = self.svd_lambdas
        v1_vec = get_col(self.svd_v, 0)
        v2_vec = get_col(self.svd_v, 1)
        left = VGroup(
            MathTex(rf"\lambda_1={tex_num(ev1)}:\quad (B^T B-{tex_num(ev1)}I)x=0"),
            MathTex(tex_matrix(sub_lambda(self.svd_ata, ev1)) + r"x=0\Rightarrow x_1=x_2"),
            MathTex(r"v_1=" + tex_column(v1_vec), color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.68)
        self.left_col(left, y=1.0, max_width=6.1)
        right = VGroup(
            MathTex(rf"\lambda_2={tex_num(ev2)}:\quad (B^T B-{tex_num(ev2)}I)x=0"),
            MathTex(tex_matrix(sub_lambda(self.svd_ata, ev2)) + r"x=0\Rightarrow x_1=-x_2"),
            MathTex(r"v_2=" + tex_column(v2_vec), color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.68).next_to(left, DOWN, buff=0.55).align_to(left, LEFT)
        axes = self.right_col(self.axes_small(), y=-0.15, max_width=4.6)
        v1 = self.arrow_vec(axes, scaled_vec(v1_vec, 2.0), GREEN, r"v_1")
        v2 = self.arrow_vec(axes, scaled_vec(v2_vec, 2.0), ORANGE, r"v_2")
        v_matrix = self.center_content(MathTex(r"V=" + tex_matrix(self.svd_v), color=YELLOW).scale(0.68), y=-2.85, max_width=7.0)

        self.play(FadeIn(title), Create(axes), run_time=1.0)
        self.write_sequence(left, wait=0.25, run_time=0.7)
        self.play(GrowArrow(v1[0]), FadeIn(v1[1]), run_time=0.8)
        self.write_sequence(right, wait=0.25, run_time=0.7)
        self.play(GrowArrow(v2[0]), FadeIn(v2[1]), run_time=0.8)
        self.play(TransformFromCopy(v1, v_matrix), TransformFromCopy(v2, v_matrix), run_time=1.1)
        self.play(Circumscribe(v_matrix, color=YELLOW), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_14_svd_sigma_u(self):
        title = self.Title("Dựng Σ và tính U", TEAL)
        v1_vec = get_col(self.svd_v, 0)
        v2_vec = get_col(self.svd_v, 1)
        u1_vec = get_col(self.svd_u, 0)
        u2_vec = get_col(self.svd_u, 1)
        sigma1, sigma2 = self.svd_sigma[0][0], self.svd_sigma[1][1]
        av1 = [row[0] * v1_vec[0] + row[1] * v1_vec[1] for row in self.svd_matrix]
        sigma = self.right_col(MathTex(r"\Sigma=" + tex_matrix(self.svd_sigma), color=YELLOW).scale(0.86), y=1.2)
        u1_steps = VGroup(
            MathTex(r"u_1=\frac{Bv_1}{\sigma_1}"),
            MathTex(r"Bv_1=" + tex_matrix(self.svd_matrix) + tex_column(v1_vec) + "=" + tex_column(av1)),
            MathTex(rf"u_1=\frac1{{{tex_num(sigma1)}}}" + tex_column(av1) + "=" + tex_column(u1_vec), color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.6)
        self.left_col(u1_steps, y=0.75, max_width=6.2)
        u2_steps = VGroup(
            MathTex(r"u_2=\frac{Bv_2}{\sigma_2}"),
            MathTex(r"u_2=" + tex_column(u2_vec), color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.68).next_to(u1_steps, DOWN, buff=0.5).align_to(u1_steps, LEFT)
        u_final = self.center_content(MathTex(r"U=" + tex_matrix(self.svd_u), color=YELLOW).scale(0.68), y=-2.85, max_width=7.0)

        self.play(FadeIn(title), Write(sigma), run_time=1.0)
        self.write_sequence(u1_steps, wait=0.35, run_time=0.8)
        self.play(Circumscribe(u1_steps[-1], color=GREEN), run_time=0.8)
        self.write_sequence(u2_steps, wait=0.35, run_time=0.8)
        self.play(TransformFromCopy(u1_steps[-1], u_final), TransformFromCopy(u2_steps[-1], u_final), run_time=1.0)
        self.play(Circumscribe(u_final, color=YELLOW), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_15_svd_final(self):
        title = self.Title("Công thức SVD hoàn chỉnh", TEAL)
        formula = self.center_content(MathTex(r"B=U\Sigma V^T", color=YELLOW).scale(1.0), y=2.0)
        numeric = MathTex(
            tex_matrix(self.svd_matrix)
            + r"="
            + tex_matrix(self.svd_u)
            + tex_matrix(self.svd_sigma)
            + tex_matrix(self.svd_v)
            + r"^T"
        ).scale(0.55)
        self.center_content(numeric, y=0.35, max_width=11.6)
        labels = VGroup(
            VGroup(MathTex(r"V^T:", color=BLUE).scale(0.5), self.VText("xoay", 22, BLUE)).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"\Sigma:", color=YELLOW).scale(0.5), self.VText("kéo giãn", 22, YELLOW)).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"U:", color=RED).scale(0.5), self.VText("xoay lại", 22, RED)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.55).to_edge(DOWN)

        self.play(FadeIn(title), run_time=0.8)
        self.play(Write(formula), run_time=1.0)
        self.play(Write(numeric), run_time=1.4)
        self.play(FadeIn(labels[0]), FadeIn(labels[1]), FadeIn(labels[2]), run_time=1.0)
        self.wait(2.5)
        self.wipe()

    def scene_16_svd_geometry(self):
        title = self.Title("Trực quan SVD: rotate - scale - rotate", TEAL).shift(DOWN * 0.16)
        formula = MathTex(r"B=U\Sigma V^T", color=YELLOW).scale(0.72).to_edge(LEFT, buff=0.78).shift(UP * 2.42)
        formula.set_stroke(BLACK, width=4, background=True)
        frame = self.camera.frame
        frame.save_state()
        axes = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8.0,
            y_length=6.0,
            background_line_style={"stroke_opacity": 0.0, "stroke_width": 1},
        ).shift(DOWN * 0.15)
        radius = 1.15
        origin = axes.c2p(0, 0)
        sample_angles = np.linspace(0, TAU, 32, endpoint=False)
        deformation_grid = VGroup(
            *[
                Line(axes.c2p(x, -3), axes.c2p(x, 3), color=BLUE_E, stroke_width=1.1).set_opacity(0.24)
                for x in np.arange(-4, 4.01, 0.5)
            ],
            *[
                Line(axes.c2p(-4, y), axes.c2p(4, y), color=TEAL_E, stroke_width=1.1).set_opacity(0.24)
                for y in np.arange(-3, 3.01, 0.5)
            ],
        )
        circle = Circle(radius=radius, color=WHITE, stroke_width=4).move_to(axes.c2p(0, 0))
        spokes = VGroup(
            *[
                Line(
                    origin,
                    axes.c2p(radius * np.cos(theta), radius * np.sin(theta)),
                    color=GRAY_B,
                    stroke_width=1,
                ).set_opacity(0.22)
                for theta in sample_angles[::2]
            ]
        )
        samples = VGroup(
            *[
                Dot(
                    axes.c2p(radius * np.cos(theta), radius * np.sin(theta)),
                    radius=0.032,
                    color=YELLOW,
                ).set_opacity(0.72)
                for theta in sample_angles
            ]
        )
        e1 = Arrow(axes.c2p(0, 0), axes.c2p(radius, 0), buff=0, color=RED, stroke_width=6)
        e2 = Arrow(axes.c2p(0, 0), axes.c2p(0, radius), buff=0, color=GREEN, stroke_width=6)
        x_data = np.array([0.95, 0.56])
        x = Arrow(axes.c2p(0, 0), axes.c2p(x_data[0], x_data[1]), buff=0, color=YELLOW, stroke_width=6)
        labels = VGroup(
            MathTex(r"e_1", color=RED).scale(0.65).next_to(e1.get_end(), DOWN, buff=0.08),
            MathTex(r"e_2", color=GREEN).scale(0.65).next_to(e2.get_end(), LEFT, buff=0.08),
            MathTex(r"x", color=YELLOW).scale(0.65).next_to(x.get_end(), UR, buff=0.08),
        )
        space = VGroup(deformation_grid, circle, spokes, samples, e1, e2, x)

        v1_vec = scaled_vec(get_col(self.svd_v, 0), 2.25)
        v2_vec = scaled_vec(get_col(self.svd_v, 1), 2.25)
        singular_lines = VGroup(
            DashedLine(axes.c2p(-v1_vec[0], -v1_vec[1]), axes.c2p(v1_vec[0], v1_vec[1]), color=BLUE, stroke_width=3, dash_length=0.18),
            DashedLine(axes.c2p(-v2_vec[0], -v2_vec[1]), axes.c2p(v2_vec[0], v2_vec[1]), color=TEAL, stroke_width=3, dash_length=0.18),
        ).set_opacity(0.85)
        singular_labels = VGroup(
            MathTex(r"v_1", color=BLUE).scale(0.65).next_to(axes.c2p(v1_vec[0], v1_vec[1]), UR, buff=0.04),
            MathTex(r"v_2", color=TEAL).scale(0.65).next_to(axes.c2p(v2_vec[0], v2_vec[1]), UL, buff=0.04),
        ).set_opacity(0.85)
        angle_arc = Arc(radius=0.62, start_angle=0, angle=PI / 4, color=BLUE, stroke_width=4).move_arc_center_to(origin)
        angle_label = MathTex(r"45^\circ", color=BLUE).scale(0.55).move_to(axes.c2p(0.78, 0.32))

        arr_vt = np.array(self.svd_vt, dtype=float)
        arr_sigma = np.array(self.svd_sigma, dtype=float)
        arr_u = np.array(self.svd_u, dtype=float)

        def apply_2d(mat):
            def func(point):
                source = np.array([point[0] - axes.c2p(0, 0)[0], point[1] - axes.c2p(0, 0)[1]])
                xy = mat @ source
                return np.array([xy[0] + axes.c2p(0, 0)[0], xy[1] + axes.c2p(0, 0)[1], point[2]])
            return func

        after_vt = space.copy().apply_function(apply_2d(arr_vt))
        after_sigma = after_vt.copy().apply_function(apply_2d(arr_sigma))
        after_u = after_sigma.copy().apply_function(apply_2d(arr_u))
        singular_lines_after_vt = singular_lines.copy().apply_function(apply_2d(arr_vt))
        sigma_outline = after_sigma[1].copy().set_color(YELLOW).set_stroke(width=6, opacity=0.95)
        final_outline = after_u[1].copy().set_color(RED).set_stroke(width=6, opacity=0.95)

        sigma1 = self.svd_sigma[0][0]
        sigma2 = self.svd_sigma[1][1]
        stretch_axes = VGroup(
            DoubleArrow(axes.c2p(-radius * sigma1, 0), axes.c2p(radius * sigma1, 0), buff=0, color=YELLOW, stroke_width=4, tip_length=0.16),
            DoubleArrow(axes.c2p(0, -radius * sigma2), axes.c2p(0, radius * sigma2), buff=0, color=TEAL, stroke_width=4, tip_length=0.16),
        )
        stretch_labels = VGroup(
            MathTex(r"\sigma_1=" + tex_num(sigma1), color=YELLOW).scale(0.65).next_to(stretch_axes[0], DOWN, buff=0.12),
            MathTex(r"\sigma_2=" + tex_num(sigma2), color=TEAL).scale(0.65).next_to(stretch_axes[1], RIGHT, buff=0.12),
        )
        final_stretch_axes = stretch_axes.copy().apply_function(apply_2d(arr_u))
        x_vt = arr_vt @ x_data
        x_sigma = arr_sigma @ x_vt
        x_final = arr_u @ x_sigma
        final_x_label = MathTex(r"Bx", color=RED).scale(0.65).next_to(axes.c2p(x_final[0], x_final[1]), UR, buff=0.06)
        phase = VGroup(
            MathTex(r"I", color=WHITE).scale(0.65),
            MathTex(r"\to", color=GRAY_A).scale(0.65),
            MathTex(r"V^T", color=GRAY_A).scale(0.65),
            MathTex(r"\to", color=GRAY_A).scale(0.65),
            MathTex(r"\Sigma", color=GRAY_A).scale(0.65),
            MathTex(r"\to", color=GRAY_A).scale(0.65),
            MathTex(r"U", color=GRAY_A).scale(0.65),
        ).arrange(RIGHT, buff=0.14).to_edge(LEFT, buff=0.78).shift(UP * 2.02)
        phase.set_stroke(BLACK, width=3, background=True)
        cap_singular = VGroup(
            self.VText("Các ưhướng", 24, TEAL),
            MathTex(r"v_1,\ v_2", color=TEAL).scale(0.5),
            self.VText("cho biết nên xoay hệ tọa độ như thế nào", 24, TEAL),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN)
        cap_vt = VGroup(
            self.VText("Bước 1:", 24, BLUE),
            MathTex(r"V^T", color=BLUE).scale(0.5),
            self.VText("đưa hai hướng singular về đúng trục tọa độ", 24, BLUE),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN)
        cap_sigma = VGroup(
            self.VText("Bước 2:", 24, YELLOW),
            MathTex(r"\Sigma", color=YELLOW).scale(0.5),
            self.VText("kéo dài theo trục", 24, YELLOW),
            MathTex(r"\sigma_1", color=YELLOW).scale(0.5),
            self.VText("và giữ trục", 24, YELLOW),
            MathTex(r"\sigma_2", color=YELLOW).scale(0.5),
            self.VText("ngắn hơn", 24, YELLOW),
        ).arrange(RIGHT, buff=0.1)
        self.fit(cap_sigma, max_width=11.2)
        cap_sigma.to_edge(DOWN)
        captions = [
            self.Explain("Bắt đầu từ đường tròn đơn vị trong hệ tọa độ chuẩn", WHITE),
            cap_singular,
            cap_vt,
            self.Explain("Lưới và đường tròn cùng xoay: toàn bộ mặt phẳng đang đổi tọa độ", BLUE),
            cap_sigma,
            self.Explain("Lưới bị kéo giãn cùng đường tròn, tạo thành ellipse", YELLOW),
            self.Explain("Bước 3: U xoay ellipse sang hệ đích của phép biến đổi B", RED),
            self.Explain("Kết quả cuối cùng là ảnh hình học của toàn bộ đường tròn đơn vị", RED),
        ]
        maps = [
            MathTex(r"x\mapsto V^Tx", color=BLUE).scale(0.62).to_edge(LEFT, buff=0.78).shift(UP * 1.62),
            MathTex(r"V^Tx\mapsto \Sigma V^Tx", color=YELLOW).scale(0.62).to_edge(LEFT, buff=0.78).shift(UP * 1.62),
            MathTex(r"\Sigma V^Tx\mapsto U\Sigma V^Tx", color=RED).scale(0.62).to_edge(LEFT, buff=0.78).shift(UP * 1.62),
        ]
        for item in maps:
            item.set_stroke(BLACK, width=4, background=True)
        final = VGroup(
            MathTex(r"B=U\Sigma V^T", color=YELLOW).scale(0.68),
            self.VText("= xoay - co giãn - xoay", 25, YELLOW),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN)

        self.play(
            FadeIn(title),
            FadeIn(formula),
            FadeIn(phase),
            Create(axes),
            Create(deformation_grid),
            Create(circle),
            Create(spokes),
            GrowArrow(e1),
            GrowArrow(e2),
            GrowArrow(x),
            FadeIn(labels),
            FadeIn(captions[0]),
            run_time=2.2,
        )
        self.play(LaggedStart(*[FadeIn(dot) for dot in samples], lag_ratio=0.025), run_time=1.2)
        self.play(frame.animate.scale(0.98), run_time=1.1, rate_func=smooth)
        self.wait(0.7)
        self.play(
            FadeOut(captions[0], shift=UP * 0.08),
            FadeIn(captions[1], shift=UP * 0.08),
            Create(singular_lines),
            FadeIn(singular_labels),
            Create(angle_arc),
            FadeIn(angle_label),
            phase[2].animate.set_color(BLUE),
            phase[0].animate.set_opacity(0.38),
            run_time=1.6,
        )
        self.wait(1.0)
        self.play(
            FadeOut(labels),
            FadeOut(angle_arc),
            FadeOut(angle_label),
            FadeOut(captions[1], shift=UP * 0.08),
            FadeIn(captions[2], shift=UP * 0.08),
            FadeIn(maps[0], shift=LEFT * 0.08),
            Transform(space, after_vt),
            Transform(singular_lines, singular_lines_after_vt),
            FadeOut(singular_labels),
            frame.animate.shift(RIGHT * 0.16).scale(0.99),
            run_time=3.4,
            rate_func=smooth,
        )
        self.play(FadeOut(captions[2], shift=UP * 0.08), FadeIn(captions[3], shift=UP * 0.08), run_time=0.8)
        self.wait(1.2)
        self.play(
            FadeOut(captions[3], shift=UP * 0.08),
            FadeIn(captions[4], shift=UP * 0.08),
            FadeOut(maps[0], shift=UP * 0.05),
            FadeIn(maps[1], shift=UP * 0.05),
            Transform(space, after_sigma),
            FadeOut(singular_lines),
            phase[4].animate.set_color(YELLOW),
            phase[2].animate.set_opacity(0.45),
            frame.animate.shift(RIGHT * 0.10).scale(0.99),
            run_time=3.8,
            rate_func=smooth,
        )
        self.play(Create(sigma_outline), Create(stretch_axes), FadeIn(stretch_labels), run_time=1.25)
        self.play(FadeOut(captions[4], shift=UP * 0.08), FadeIn(captions[5], shift=UP * 0.08), run_time=0.8)
        self.wait(1.3)
        self.play(
            FadeOut(captions[5], shift=UP * 0.08),
            FadeIn(captions[6], shift=UP * 0.08),
            FadeOut(maps[1], shift=UP * 0.05),
            FadeIn(maps[2], shift=UP * 0.05),
            Transform(space, after_u),
            Transform(stretch_axes, final_stretch_axes),
            FadeOut(stretch_labels),
            FadeOut(sigma_outline),
            phase[6].animate.set_color(RED),
            phase[4].animate.set_opacity(0.45),
            frame.animate.shift(LEFT * 0.26).scale(1.03),
            run_time=3.6,
            rate_func=smooth,
        )
        self.play(Create(final_outline), FadeIn(final_x_label), run_time=1.1)
        self.play(FadeOut(captions[6], shift=UP * 0.08), FadeIn(captions[7], shift=UP * 0.08), run_time=0.8)
        self.wait(1.6)
        self.play(Restore(frame), run_time=1.2, rate_func=smooth)
        self.play(
            FadeOut(captions[7], shift=UP * 0.08),
            FadeIn(final, shift=UP * 0.08),
            FadeOut(maps[2]),
            FadeOut(stretch_axes),
            FadeOut(final_outline),
            FadeOut(final_x_label),
            FadeOut(phase),
            run_time=1.2,
        )
        self.wait(3.0)
        self.wipe()
