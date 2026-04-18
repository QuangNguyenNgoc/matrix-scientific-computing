from manim import *
import numpy as np

from decomposition import svdDecomp
from diagonalization import diagonalize, matrixMultiply, matrixTranspose


SVD_MATRIX = [[2.0, 1.0], [0.5, 1.5]]
DIAG_MATRIX = [[4.0, 1.0], [2.0, 3.0]]
FONT = "DejaVu Sans Mono"
BG = "#0f1217"
CARD_BG = "#171b24"
CARD_STROKE = "#3a4252"
NORMAL_WEIGHT = "NORMAL"
BOLD_WEIGHT = "BOLD"


def fmt_num(value):
    value = 0.0 if abs(float(value)) < 1e-9 else float(value)
    if abs(value - round(value)) < 1e-9:
        return f"{value:.0f}"
    return f"{value:.2f}"


def fmt_sci(value):
    return f"{float(value):.2e}"


def as_list(matrix):
    if isinstance(matrix, np.ndarray):
        return matrix.tolist()
    return [list(row) for row in matrix]


def np_matrix(matrix):
    return np.array(matrix, dtype=float)


def fit_width(mobject, width):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def text_block(text, font_size=26, color=WHITE, weight=NORMAL_WEIGHT):
    return Text(
        text,
        font=FONT,
        font_size=font_size,
        line_spacing=0.78,
        color=color,
        weight=weight,
    )


def formula_card(title, formula, accent=BLUE_B, detail=None, width=None):
    title_mob = text_block(title, font_size=20, color=accent, weight=BOLD_WEIGHT)
    formula_mob = text_block(formula, font_size=25, color=WHITE)
    content = VGroup(title_mob, formula_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    if detail:
        detail_mob = text_block(detail, font_size=18, color=GRAY_A)
        content.add(detail_mob)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    if width:
        fit_width(content, width - 0.45)
    bg = SurroundingRectangle(content, buff=0.18, corner_radius=0.06)
    bg.set_fill(CARD_BG, opacity=0.92)
    bg.set_stroke(accent, width=1.5, opacity=0.85)
    return VGroup(bg, content)


def matrix_card(name, matrix, accent=WHITE, font_size=18, title_size=20, cell_w=0.72, cell_h=0.38):
    rows = as_list(matrix)
    title = text_block(name, font_size=title_size, color=accent, weight=BOLD_WEIGHT)

    row_groups = []
    for row in rows:
        cells = []
        for value in row:
            box = Rectangle(width=cell_w, height=cell_h)
            box.set_fill(BG, opacity=0.16)
            box.set_stroke(CARD_STROKE, width=0.75, opacity=0.55)
            number = text_block(f"{fmt_num(value):>5}", font_size=font_size, color=WHITE)
            number.move_to(box)
            cells.append(VGroup(box, number))
        row_groups.append(VGroup(*cells).arrange(RIGHT, buff=0.03))

    table = VGroup(*row_groups).arrange(DOWN, buff=0.04)
    top = table.get_top()[1] + 0.09
    bottom = table.get_bottom()[1] - 0.09
    left = table.get_left()[0] - 0.13
    right = table.get_right()[0] + 0.13
    tick = 0.13
    left_bracket = VGroup(
        Line([left, top, 0], [left, bottom, 0]),
        Line([left, top, 0], [left + tick, top, 0]),
        Line([left, bottom, 0], [left + tick, bottom, 0]),
    ).set_color(accent)
    right_bracket = VGroup(
        Line([right, top, 0], [right, bottom, 0]),
        Line([right - tick, top, 0], [right, top, 0]),
        Line([right - tick, bottom, 0], [right, bottom, 0]),
    ).set_color(accent)
    bracketed = VGroup(left_bracket, table, right_bracket)

    content = VGroup(title, bracketed).arrange(DOWN, buff=0.12)
    bg = SurroundingRectangle(content, buff=0.16, corner_radius=0.06)
    bg.set_fill(CARD_BG, opacity=0.9)
    bg.set_stroke(accent, width=1.25, opacity=0.75)
    card = VGroup(bg, content)
    return card


def bullet_panel(title, bullets, accent=BLUE_B, font_size=20, width=6.0):
    title_mob = text_block(title, font_size=23, color=accent, weight=BOLD_WEIGHT)
    lines = []
    for bullet in bullets:
        dot = Dot(radius=0.045, color=accent)
        line = text_block(bullet, font_size=font_size, color=GRAY_A)
        fit_width(line, width - 0.55)
        rows = VGroup(dot, line).arrange(RIGHT, buff=0.14, aligned_edge=UP)
        lines.append(rows)
    body = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fit_width(content, width)
    bg = SurroundingRectangle(content, buff=0.2, corner_radius=0.06)
    bg.set_fill(CARD_BG, opacity=0.9)
    bg.set_stroke(accent, width=1.25, opacity=0.7)
    return VGroup(bg, content)


def chapter_header(index, title, subtitle, accent=BLUE_B):
    index_mob = text_block(f"{index:02d}", font_size=26, color=BG, weight=BOLD_WEIGHT)
    badge = RoundedRectangle(width=0.72, height=0.46, corner_radius=0.05)
    badge.set_fill(accent, opacity=1.0)
    badge.set_stroke(accent, width=0)
    index_group = VGroup(badge, index_mob)
    index_mob.move_to(badge)

    title_mob = text_block(title, font_size=31, color=WHITE, weight=BOLD_WEIGHT)
    subtitle_mob = text_block(subtitle, font_size=18, color=GRAY_A)
    title_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    header = VGroup(index_group, title_group).arrange(RIGHT, buff=0.24, aligned_edge=UP)
    header.to_edge(UP).to_edge(LEFT)
    return header


def make_plane():
    return NumberPlane(
        x_range=[-4, 4, 1],
        y_range=[-3, 3, 1],
        x_length=7.0,
        y_length=5.35,
        background_line_style={
            "stroke_color": GRAY_C,
            "stroke_width": 1.0,
            "stroke_opacity": 0.32,
        },
        axis_config={"stroke_color": GRAY_A, "stroke_width": 2},
    ).to_edge(LEFT).shift(DOWN * 0.25)


def transform_points(points, matrix):
    arr = np.array(points, dtype=float)
    mat = np.array(matrix, dtype=float)
    return arr @ mat.T


def transform_vector(vector, matrix):
    vec = np.array(vector, dtype=float)
    mat = np.array(matrix, dtype=float)
    return mat @ vec


def unit_circle_points(count=260):
    angles = np.linspace(0.0, 2.0 * np.pi, count, endpoint=False)
    return np.column_stack((np.cos(angles), np.sin(angles)))


def curve_from_points(plane, points, color=BLUE_B, stroke_width=5, stroke_opacity=1.0):
    coords = [plane.c2p(float(x), float(y)) for x, y in points]
    curve = VMobject(color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
    curve.set_points_smoothly(coords + [coords[0]])
    return curve


def arrow_from_vector(plane, vector, color, width=7):
    end = plane.c2p(float(vector[0]), float(vector[1]))
    return Arrow(
        start=plane.c2p(0.0, 0.0),
        end=end,
        buff=0.0,
        stroke_width=width,
        max_tip_length_to_length_ratio=0.14,
        color=color,
    )


def vector_pair_visual(plane, vec1, vec2, label1, label2, color1=BLUE_B, color2=GREEN_B):
    arrow1 = arrow_from_vector(plane, vec1, color1)
    arrow2 = arrow_from_vector(plane, vec2, color2)
    text1 = text_block(label1, font_size=18, color=color1).next_to(arrow1.get_end(), UR, buff=0.08)
    text2 = text_block(label2, font_size=18, color=color2).next_to(arrow2.get_end(), DR, buff=0.08)
    return VGroup(arrow1, arrow2, text1, text2)


def multiply_chain(*matrices):
    result = as_list(matrices[0])
    for matrix in matrices[1:]:
        result = matrixMultiply(result, as_list(matrix))
    return result


def max_abs_error(mat_a, mat_b):
    arr_a = np.array(mat_a, dtype=float)
    arr_b = np.array(mat_b, dtype=float)
    return float(np.max(np.abs(arr_a - arr_b)))


def approximate_runtime_seconds():
    return 518


class Part2ManimDemo(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.show_title_and_scope()
        self.show_problem_setup()
        svd_data = self.get_svd_data()
        self.show_svd_relation_to_ata(svd_data)
        self.show_svd_geometry(svd_data)
        self.show_svd_numeric_breakdown(svd_data)
        diag_data = self.get_diag_data()
        self.show_diagonalization_theory(diag_data)
        self.show_diagonalization_geometry(diag_data)
        self.show_coordinate_change_example(diag_data)
        self.show_diagonalization_verification(diag_data)
        self.show_closing()

    def get_svd_data(self):
        mat_u, mat_sigma, mat_vt = svdDecomp(SVD_MATRIX)
        mat_v = matrixTranspose(mat_vt)
        mat_at = matrixTranspose(SVD_MATRIX)
        mat_ata = matrixMultiply(mat_at, SVD_MATRIX)
        return {
            "a": SVD_MATRIX,
            "at": mat_at,
            "ata": mat_ata,
            "u": mat_u,
            "sigma": mat_sigma,
            "v": mat_v,
            "vt": mat_vt,
            "sigmas": [mat_sigma[i][i] for i in range(2)],
        }

    def get_diag_data(self):
        mat_p, mat_d, mat_p_inv = diagonalize(DIAG_MATRIX)
        return {
            "a": DIAG_MATRIX,
            "p": mat_p,
            "d": mat_d,
            "p_inv": mat_p_inv,
            "lambdas": [mat_d[i][i] for i in range(2)],
        }

    def show_title_and_scope(self):
        title = text_block("PART 2: MATRIX DECOMPOSITION", font_size=43, color=WHITE, weight=BOLD_WEIGHT)
        subtitle = formula_card(
            "Video target",
            "SVD geometry  +  Diagonalization A = P D P^-1",
            accent=BLUE_B,
            detail="A Manim demonstration built from the local Python implementation.",
            width=10.5,
        )
        checklist = bullet_panel(
            "Rubric coverage",
            [
                "Introduce a concrete matrix A and state the selected decomposition.",
                "Visualize SVD as rotate -> scale -> rotate on the unit circle.",
                "Display eigenvalues, eigenvectors, and the factorization A = P D P^-1.",
                "Verify the decompositions numerically with reconstruction errors.",
            ],
            accent=GREEN_B,
            font_size=20,
            width=8.8,
        )
        runtime = formula_card(
            "Planned length",
            "About 8 minutes 40 seconds",
            accent=YELLOW_B,
            detail="Longer than the 2 minute minimum and far below the 30 minute limit.",
            width=7.8,
        )
        group = VGroup(title, subtitle, checklist, runtime).arrange(DOWN, buff=0.35)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=3.0)
        self.play(FadeIn(subtitle), run_time=3.5)
        self.play(FadeIn(checklist, shift=UP * 0.1), run_time=4.0)
        self.play(FadeIn(runtime), run_time=2.5)
        self.wait(12)
        self.play(FadeOut(group), run_time=3.0)

    def show_problem_setup(self):
        header = chapter_header(
            1,
            "Problem Setup",
            "Choose SVD as the decomposition method, then also show diagonalization.",
            accent=BLUE_B,
        )
        svd_card = matrix_card("A_svd", SVD_MATRIX, accent=BLUE_B, font_size=20)
        svd_goal = formula_card(
            "SVD goal",
            "A_svd = U Sigma V^T",
            accent=BLUE_B,
            detail="U and V are orthogonal; Sigma stores the singular values.",
            width=5.3,
        )
        diag_card = matrix_card("A_diag", DIAG_MATRIX, accent=GREEN_B, font_size=20)
        diag_goal = formula_card(
            "Diagonalization goal",
            "A_diag = P D P^-1",
            accent=GREEN_B,
            detail="Columns of P are eigenvectors; D stores eigenvalues.",
            width=5.3,
        )
        left = VGroup(svd_card, svd_goal).arrange(DOWN, buff=0.28)
        right = VGroup(diag_card, diag_goal).arrange(DOWN, buff=0.28)
        panels = VGroup(left, right).arrange(RIGHT, buff=1.0).shift(DOWN * 0.25)
        source = formula_card(
            "Implementation boundary",
            "svdDecomp(A) from decomposition.py   |   diagonalize(A) from diagonalization.py",
            accent=GRAY_B,
            detail="This Manim file only visualizes and formats the computed results.",
            width=11.6,
        ).to_edge(DOWN)

        self.play(FadeIn(header), run_time=2.5)
        self.play(FadeIn(panels), run_time=4.0)
        self.play(FadeIn(source), run_time=3.0)
        self.wait(16)
        self.play(FadeOut(VGroup(header, panels, source)), run_time=3.0)

    def show_svd_relation_to_ata(self, svd_data):
        header = chapter_header(
            2,
            "How SVD Is Built",
            "The implementation uses A^T A to obtain right singular vectors and singular values.",
            accent=TEAL_B,
        )
        sigma_1, sigma_2 = svd_data["sigmas"]
        lambda_diag = [[sigma_1**2, 0.0], [0.0, sigma_2**2]]

        cards = VGroup(
            matrix_card("A", svd_data["a"], accent=WHITE, font_size=18),
            matrix_card("A^T A", svd_data["ata"], accent=TEAL_B, font_size=18),
            matrix_card("V", svd_data["v"], accent=BLUE_B, font_size=18),
            matrix_card("Lambda", lambda_diag, accent=YELLOW_B, font_size=18),
        ).arrange(RIGHT, buff=0.35).scale(0.87).shift(UP * 0.75)
        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.12, color=GRAY_B, stroke_width=4))

        formula = formula_card(
            "Key relation",
            "A^T A = V Lambda V^T,     sigma_i = sqrt(lambda_i)",
            accent=TEAL_B,
            detail="SVD is closely linked to diagonalizing the symmetric matrix A^T A.",
            width=10.5,
        )
        steps = bullet_panel(
            "Algorithm shown by the scene",
            [
                "Form A^T A using the local matrixMultiply and matrixTranspose helpers.",
                "Find eigenvectors of A^T A; these vectors become the columns of V.",
                "Take square roots of eigenvalues to obtain singular values sigma_i.",
                "Compute left singular vectors using u_i = A v_i / sigma_i.",
            ],
            accent=TEAL_B,
            font_size=18,
            width=9.4,
        )
        explanation = VGroup(formula, steps).arrange(DOWN, buff=0.18).to_edge(DOWN)

        self.play(FadeIn(header), run_time=2.5)
        self.play(FadeIn(cards), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=5.5)
        self.play(FadeIn(formula), run_time=3.0)
        self.play(FadeIn(steps), run_time=4.0)
        self.wait(20)
        self.play(FadeOut(VGroup(header, cards, arrows, explanation)), run_time=3.0)

    def show_svd_geometry(self, svd_data):
        mat_u = svd_data["u"]
        mat_sigma = svd_data["sigma"]
        mat_vt = svd_data["vt"]
        arr_a = np_matrix(svd_data["a"])

        header = chapter_header(
            3,
            "SVD Geometry",
            "A circle becomes an ellipse through rotate -> scale -> rotate.",
            accent=BLUE_B,
        )
        pipeline = formula_card(
            "Transformation pipeline",
            "x  ->  V^T x  ->  Sigma V^T x  ->  U Sigma V^T x = A x",
            accent=BLUE_B,
            detail="The same point is transformed step by step, so the geometry is visible.",
            width=10.7,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.25)
        plane = make_plane()

        matrix_panel = VGroup(
            matrix_card("V^T", mat_vt, accent=TEAL_B, font_size=15, cell_w=0.66),
            matrix_card("Sigma", mat_sigma, accent=YELLOW_B, font_size=15, cell_w=0.66),
            matrix_card("U", mat_u, accent=RED_B, font_size=15, cell_w=0.66),
            formula_card(
                "Singular values",
                f"sigma_1 = {fmt_num(svd_data['sigmas'][0])}\nsigma_2 = {fmt_num(svd_data['sigmas'][1])}",
                accent=YELLOW_B,
                detail="They are the stretch factors of the ellipse.",
                width=3.45,
            ),
        ).arrange(DOWN, buff=0.12).to_edge(RIGHT).shift(DOWN * 0.05)
        matrix_panel.scale_to_fit_height(6.35)

        points_0 = unit_circle_points()
        points_1 = transform_points(points_0, mat_vt)
        points_2 = transform_points(points_1, mat_sigma)
        points_3 = transform_points(points_2, mat_u)
        points_direct = transform_points(points_0, arr_a)

        shape = curve_from_points(plane, points_0, color=BLUE_B, stroke_width=5)
        shape_vt = curve_from_points(plane, points_1, color=TEAL_B, stroke_width=5)
        shape_sigma = curve_from_points(plane, points_2, color=YELLOW_B, stroke_width=5)
        shape_u = curve_from_points(plane, points_3, color=RED_B, stroke_width=5)
        shape_direct = curve_from_points(plane, points_direct, color=PURPLE_B, stroke_width=4, stroke_opacity=0.85)

        e1 = np.array([1.0, 0.0], dtype=float)
        e2 = np.array([0.0, 1.0], dtype=float)
        vt_e1 = transform_vector(e1, mat_vt)
        vt_e2 = transform_vector(e2, mat_vt)
        sg_e1 = transform_vector(vt_e1, mat_sigma)
        sg_e2 = transform_vector(vt_e2, mat_sigma)
        u_e1 = transform_vector(sg_e1, mat_u)
        u_e2 = transform_vector(sg_e2, mat_u)

        basis = vector_pair_visual(plane, e1, e2, "e1", "e2", BLUE_B, GREEN_B)
        basis_vt = vector_pair_visual(plane, vt_e1, vt_e2, "V^T e1", "V^T e2", BLUE_B, GREEN_B)
        basis_sigma = vector_pair_visual(plane, sg_e1, sg_e2, "Sigma V^T e1", "Sigma V^T e2", BLUE_B, GREEN_B)
        basis_u = vector_pair_visual(plane, u_e1, u_e2, "A e1", "A e2", BLUE_B, GREEN_B)

        note = formula_card(
            "Start",
            "Unit circle: ||x|| = 1",
            accent=BLUE_B,
            detail="Every point on the circle is a possible input direction.",
            width=7.4,
        ).to_edge(DOWN)
        focus = SurroundingRectangle(matrix_panel[0], color=TEAL_B, buff=0.07, stroke_width=3)

        self.play(FadeIn(header), FadeIn(pipeline), Create(plane), FadeIn(matrix_panel), run_time=6.0)
        self.play(Create(shape), FadeIn(basis), FadeIn(note), run_time=6.0)
        self.wait(12)

        note_vt = formula_card(
            "Step 1: right rotation",
            "V^T rotates the input directions.",
            accent=TEAL_B,
            detail="The circle remains a circle because rotations preserve length.",
            width=7.4,
        ).move_to(note)
        self.play(Create(focus), run_time=1.5)
        self.play(
            Transform(shape, shape_vt),
            ReplacementTransform(basis, basis_vt),
            ReplacementTransform(note, note_vt),
            run_time=8.0,
        )
        basis = basis_vt
        note = note_vt
        self.wait(14)

        note_sigma = formula_card(
            "Step 2: axis scaling",
            "Sigma stretches by sigma_1 and sigma_2.",
            accent=YELLOW_B,
            detail="The unit circle becomes an ellipse after unequal scaling.",
            width=7.4,
        ).move_to(note)
        self.play(Transform(focus, SurroundingRectangle(matrix_panel[1], color=YELLOW_B, buff=0.07, stroke_width=3)), run_time=2.0)
        self.play(
            Transform(shape, shape_sigma),
            ReplacementTransform(basis, basis_sigma),
            ReplacementTransform(note, note_sigma),
            run_time=8.0,
        )
        basis = basis_sigma
        note = note_sigma
        self.wait(14)

        note_u = formula_card(
            "Step 3: left rotation",
            "U rotates the scaled ellipse into the final position.",
            accent=RED_B,
            detail="The final shape is exactly the image of the unit circle under A.",
            width=7.4,
        ).move_to(note)
        self.play(Transform(focus, SurroundingRectangle(matrix_panel[2], color=RED_B, buff=0.07, stroke_width=3)), run_time=2.0)
        self.play(
            Transform(shape, shape_u),
            ReplacementTransform(basis, basis_u),
            ReplacementTransform(note, note_u),
            run_time=8.0,
        )
        basis = basis_u
        note = note_u
        self.wait(14)

        compare = formula_card(
            "Consistency check",
            "Direct transform by A overlaps U Sigma V^T.",
            accent=PURPLE_B,
            detail="The purple curve is computed from A x directly.",
            width=7.4,
        ).move_to(note)
        self.play(Create(shape_direct), ReplacementTransform(note, compare), run_time=5.0)
        self.play(
            Indicate(shape, color=RED_B, scale_factor=1.03),
            Indicate(shape_direct, color=PURPLE_B, scale_factor=1.03),
            run_time=4.0,
        )
        self.wait(16)
        self.play(FadeOut(VGroup(header, pipeline, plane, matrix_panel, shape, shape_direct, basis, focus, compare)), run_time=3.0)

    def show_svd_numeric_breakdown(self, svd_data):
        mat_u = svd_data["u"]
        mat_sigma = svd_data["sigma"]
        mat_vt = svd_data["vt"]
        arr_a = np_matrix(svd_data["a"])
        arr_u = np_matrix(mat_u)
        arr_vt = np_matrix(mat_vt)
        arr_rebuild = np_matrix(multiply_chain(mat_u, mat_sigma, mat_vt))
        err = max_abs_error(arr_a, arr_rebuild)

        sigma_1, sigma_2 = svd_data["sigmas"]
        term_1 = sigma_1 * np.outer(arr_u[:, 0], arr_vt[0, :])
        term_2 = sigma_2 * np.outer(arr_u[:, 1], arr_vt[1, :])
        term_sum = term_1 + term_2
        rank1_error = max_abs_error(arr_a, term_1)

        header = chapter_header(
            4,
            "SVD Numerical Check",
            "After the geometry, verify the same decomposition with numbers.",
            accent=YELLOW_B,
        )
        formula = formula_card(
            "Outer product view",
            "A = sigma_1 u_1 v_1^T + sigma_2 u_2 v_2^T",
            accent=YELLOW_B,
            detail="Each term adds one directional component of the matrix.",
            width=10.5,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.25)

        cards_top = VGroup(
            matrix_card("A", arr_a, accent=WHITE, font_size=17),
            matrix_card("U Sigma V^T", arr_rebuild, accent=GREEN_B, font_size=17),
            formula_card("Rebuild error", f"max error = {fmt_sci(err)}", accent=GREEN_B, width=3.3),
        ).arrange(RIGHT, buff=0.36).shift(UP * 0.55)
        cards_top.scale_to_fit_width(11.5)

        cards_bottom = VGroup(
            matrix_card("Term 1", term_1, accent=BLUE_B, font_size=16),
            matrix_card("Term 2", term_2, accent=TEAL_B, font_size=16),
            matrix_card("Term 1 + Term 2", term_sum, accent=GREEN_B, font_size=16),
            formula_card("Rank-1 loss", f"rank-1 error = {fmt_sci(rank1_error)}", accent=YELLOW_B, width=3.25),
        ).arrange(RIGHT, buff=0.25).shift(DOWN * 1.45)
        cards_bottom.scale_to_fit_width(12.0)

        note = bullet_panel(
            "Interpretation",
            [
                "The full two-term sum reconstructs A with only floating-point error.",
                "Keeping only term 1 gives the best one-direction approximation.",
                "This is why SVD is useful for compression and low-rank approximation.",
            ],
            accent=YELLOW_B,
            font_size=18,
            width=8.8,
        ).to_edge(DOWN)

        self.play(FadeIn(header), FadeIn(formula), run_time=4.5)
        self.play(FadeIn(cards_top), run_time=5.0)
        self.wait(12)
        self.play(FadeIn(cards_bottom), run_time=6.0)
        self.play(FadeIn(note), run_time=4.0)
        self.wait(20)
        self.play(FadeOut(VGroup(header, formula, cards_top, cards_bottom, note)), run_time=3.0)

    def show_diagonalization_theory(self, diag_data):
        header = chapter_header(
            5,
            "Diagonalization Setup",
            "A diagonalizable matrix has an eigenbasis.",
            accent=GREEN_B,
        )
        mat_p = diag_data["p"]
        mat_d = diag_data["d"]
        mat_p_inv = diag_data["p_inv"]
        lambdas = diag_data["lambdas"]
        det_p = float(np.linalg.det(np_matrix(mat_p)))

        top = VGroup(
            matrix_card("A", diag_data["a"], accent=WHITE, font_size=18),
            matrix_card("P", mat_p, accent=BLUE_B, font_size=18),
            matrix_card("D", mat_d, accent=GREEN_B, font_size=18),
            matrix_card("P^-1", mat_p_inv, accent=GRAY_B, font_size=18),
        ).arrange(RIGHT, buff=0.28).shift(UP * 0.65)
        top.scale_to_fit_width(11.7)

        formula = formula_card(
            "Main formula",
            "A = P D P^-1",
            accent=GREEN_B,
            detail=f"lambda_1 = {fmt_num(lambdas[0])}, lambda_2 = {fmt_num(lambdas[1])}, det(P) = {fmt_num(det_p)}",
            width=6.6,
        )
        bullets = bullet_panel(
            "Meaning of the factors",
            [
                "P changes coordinates from eigenbasis coordinates back to standard coordinates.",
                "D scales each eigenbasis coordinate independently by lambda_i.",
                "P^-1 converts a vector from standard coordinates into the eigenbasis.",
            ],
            accent=GREEN_B,
            font_size=18,
            width=6.8,
        )
        middle = VGroup(formula, bullets).arrange(RIGHT, buff=0.55).shift(DOWN * 1.15)

        self.play(FadeIn(header), run_time=2.5)
        self.play(FadeIn(top), run_time=5.5)
        self.play(FadeIn(formula), run_time=3.0)
        self.play(FadeIn(bullets), run_time=4.0)
        self.wait(22)
        self.play(FadeOut(VGroup(header, top, middle)), run_time=3.0)

    def show_diagonalization_geometry(self, diag_data):
        arr_a = np_matrix(diag_data["a"])
        arr_p = np_matrix(diag_data["p"])
        lambdas = diag_data["lambdas"]

        header = chapter_header(
            6,
            "Eigenvector Geometry",
            "Eigenvectors keep their direction; eigenvalues only scale them.",
            accent=GREEN_B,
        )
        relation_card = formula_card(
            "Eigenvector rule",
            "A v_i = lambda_i v_i",
            accent=GREEN_B,
            detail="This is the visual reason diagonalization works.",
            width=6.7,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.22)
        plane = make_plane()
        panel = VGroup(
            matrix_card("P = [v1  v2]", diag_data["p"], accent=BLUE_B, font_size=16, cell_w=0.66),
            matrix_card("D", diag_data["d"], accent=GREEN_B, font_size=16, cell_w=0.66),
            formula_card(
                "Eigenvalues",
                f"lambda_1 = {fmt_num(lambdas[0])}\nlambda_2 = {fmt_num(lambdas[1])}",
                accent=YELLOW_B,
                detail="These are the scale factors along v1 and v2.",
                width=3.5,
            ),
        ).arrange(DOWN, buff=0.16).to_edge(RIGHT).shift(DOWN * 0.15)
        panel.scale_to_fit_height(5.9)

        v1 = arr_p[:, 0] / np.linalg.norm(arr_p[:, 0]) * 0.8
        v2 = arr_p[:, 1] / np.linalg.norm(arr_p[:, 1]) * 0.8
        av1 = arr_a @ v1
        av2 = arr_a @ v2

        line1 = DashedLine(
            plane.c2p(float(-3.3 * v1[0]), float(-3.3 * v1[1])),
            plane.c2p(float(3.3 * v1[0]), float(3.3 * v1[1])),
            color=BLUE_D,
            stroke_opacity=0.58,
        )
        line2 = DashedLine(
            plane.c2p(float(-3.3 * v2[0]), float(-3.3 * v2[1])),
            plane.c2p(float(3.3 * v2[0]), float(3.3 * v2[1])),
            color=TEAL_D,
            stroke_opacity=0.58,
        )
        eigen_vectors = vector_pair_visual(plane, v1, v2, "v1", "v2", BLUE_B, TEAL_B)
        transformed = vector_pair_visual(plane, av1, av2, "A v1", "A v2", RED_B, YELLOW_B)

        note_1 = formula_card(
            "Step 1",
            "Draw the eigenvector directions.",
            accent=BLUE_B,
            detail="These directions define the columns of P.",
            width=7.2,
        ).to_edge(DOWN)
        note_2 = formula_card(
            "Step 2",
            "Apply A. The arrows get longer, but stay on the same lines.",
            accent=GREEN_B,
            detail=f"A v1 = {fmt_num(lambdas[0])} v1,    A v2 = {fmt_num(lambdas[1])} v2",
            width=7.2,
        ).move_to(note_1)

        self.play(FadeIn(header), FadeIn(relation_card), Create(plane), FadeIn(panel), run_time=6.0)
        self.play(Create(line1), Create(line2), FadeIn(eigen_vectors), FadeIn(note_1), run_time=7.0)
        self.wait(16)
        self.play(FadeIn(transformed), ReplacementTransform(note_1, note_2), run_time=7.0)
        self.play(Indicate(transformed, color=GREEN_B, scale_factor=1.02), run_time=4.0)
        self.wait(18)
        self.play(FadeOut(VGroup(header, relation_card, plane, panel, line1, line2, eigen_vectors, transformed, note_2)), run_time=3.0)

    def show_coordinate_change_example(self, diag_data):
        header = chapter_header(
            7,
            "Coordinate Change View",
            "Diagonalization is easiest to understand as three simple coordinate operations.",
            accent=TEAL_B,
        )
        mat_p = diag_data["p"]
        mat_d = diag_data["d"]
        mat_p_inv = diag_data["p_inv"]
        sample_x = [[1.0], [1.0]]
        eigen_coords = matrixMultiply(mat_p_inv, sample_x)
        scaled_coords = matrixMultiply(mat_d, eigen_coords)
        final_x = matrixMultiply(mat_p, scaled_coords)
        direct_x = matrixMultiply(diag_data["a"], sample_x)

        chain_formula = formula_card(
            "For one sample vector x",
            "x  ->  P^-1 x  ->  D(P^-1 x)  ->  P D P^-1 x",
            accent=TEAL_B,
            detail="The last vector equals A x.",
            width=10.8,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.25)

        cards = VGroup(
            matrix_card("x", sample_x, accent=WHITE, font_size=17, cell_w=0.7),
            matrix_card("P^-1 x", eigen_coords, accent=GRAY_B, font_size=17, cell_w=0.7),
            matrix_card("D(P^-1 x)", scaled_coords, accent=GREEN_B, font_size=17, cell_w=0.7),
            matrix_card("P D P^-1 x", final_x, accent=BLUE_B, font_size=17, cell_w=0.7),
            matrix_card("A x", direct_x, accent=YELLOW_B, font_size=17, cell_w=0.7),
        ).arrange(RIGHT, buff=0.25).shift(UP * 0.35)
        cards.scale_to_fit_width(12.0)
        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.09, color=GRAY_B, stroke_width=4))

        explanation = bullet_panel(
            "Why this matters",
            [
                "P^-1 rewrites x using eigenvector coordinates.",
                "D applies only independent scalar multiplications.",
                "P converts the scaled coordinates back to the standard plane.",
                "This explains A^k = P D^k P^-1 for repeated powers.",
            ],
            accent=TEAL_B,
            font_size=19,
            width=8.7,
        ).to_edge(DOWN)

        self.play(FadeIn(header), FadeIn(chain_formula), run_time=4.0)
        self.play(FadeIn(cards[0]), run_time=2.0)
        for idx, arrow in enumerate(arrows):
            self.play(GrowArrow(arrow), FadeIn(cards[idx + 1]), run_time=3.2)
            self.wait(2)
        self.play(FadeIn(explanation), run_time=4.0)
        self.wait(22)
        self.play(FadeOut(VGroup(header, chain_formula, cards, arrows, explanation)), run_time=3.0)

    def show_diagonalization_verification(self, diag_data):
        mat_p = diag_data["p"]
        mat_d = diag_data["d"]
        mat_p_inv = diag_data["p_inv"]

        arr_a = np_matrix(diag_data["a"])
        arr_rebuild = np_matrix(multiply_chain(mat_p, mat_d, mat_p_inv))
        err_rebuild = max_abs_error(arr_a, arr_rebuild)

        arr_d = np_matrix(mat_d)
        arr_p = np_matrix(mat_p)
        arr_p_inv = np_matrix(mat_p_inv)
        arr_a3_direct = np.linalg.matrix_power(arr_a, 3)
        arr_d3 = np.linalg.matrix_power(arr_d, 3)
        arr_a3_diag = arr_p @ arr_d3 @ arr_p_inv
        err_power = max_abs_error(arr_a3_direct, arr_a3_diag)

        header = chapter_header(
            8,
            "Diagonalization Check",
            "Verify A = P D P^-1 and show the power shortcut.",
            accent=YELLOW_B,
        )
        formula = formula_card(
            "Power formula",
            "A^3 = P D^3 P^-1",
            accent=YELLOW_B,
            detail="Only D needs to be powered; diagonal powers are cheap.",
            width=7.0,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.25)

        top = VGroup(
            matrix_card("A", arr_a, accent=WHITE, font_size=17),
            matrix_card("P D P^-1", arr_rebuild, accent=GREEN_B, font_size=17),
            formula_card("Error", f"max = {fmt_sci(err_rebuild)}", accent=GREEN_B, width=2.8),
        ).arrange(RIGHT, buff=0.36).shift(UP * 0.45)
        top.scale_to_fit_width(11.2)

        bottom = VGroup(
            matrix_card("D^3", arr_d3, accent=YELLOW_B, font_size=16),
            matrix_card("P D^3 P^-1", arr_a3_diag, accent=BLUE_B, font_size=16),
            matrix_card("A^3 direct", arr_a3_direct, accent=WHITE, font_size=16),
            formula_card("Power error", f"max = {fmt_sci(err_power)}", accent=GREEN_B, width=2.9),
        ).arrange(RIGHT, buff=0.24).shift(DOWN * 1.35)
        bottom.scale_to_fit_width(12.0)

        note = bullet_panel(
            "Takeaway",
            [
                "The reconstruction error is tiny, so the computed factors reproduce A.",
                "For powers, D^3 is just cubing the diagonal entries.",
                "This is the practical benefit of diagonalization in scientific computing.",
            ],
            accent=YELLOW_B,
            font_size=18,
            width=8.9,
        ).to_edge(DOWN)

        self.play(FadeIn(header), FadeIn(formula), run_time=4.0)
        self.play(FadeIn(top), run_time=5.0)
        self.wait(12)
        self.play(FadeIn(bottom), run_time=6.0)
        self.play(FadeIn(note), run_time=4.0)
        self.wait(22)
        self.play(FadeOut(VGroup(header, formula, top, bottom, note)), run_time=3.0)

    def show_closing(self):
        title = text_block("Summary", font_size=40, color=WHITE, weight=BOLD_WEIGHT)
        summary = bullet_panel(
            "What the video covered",
            [
                "A concrete matrix was introduced for SVD and another for diagonalization.",
                "SVD was visualized as V^T rotation, Sigma scaling, and U rotation.",
                "The matrix A was reconstructed from U Sigma V^T and checked numerically.",
                "Eigenvalues and eigenvectors were shown through A v_i = lambda_i v_i.",
                "A = P D P^-1 and A^3 = P D^3 P^-1 were verified with error values.",
            ],
            accent=GREEN_B,
            font_size=20,
            width=9.7,
        )
        implementation = formula_card(
            "Code boundary",
            "Manim = visualization, local Python files = matrix algorithms",
            accent=BLUE_B,
            detail="The core SVD and diagonalization computations are not reimplemented here.",
            width=9.4,
        )
        runtime = formula_card(
            "Approximate runtime",
            f"{approximate_runtime_seconds() // 60} min {approximate_runtime_seconds() % 60} sec",
            accent=YELLOW_B,
            detail="Long enough for the assignment requirement and still concise.",
            width=5.4,
        )
        group = VGroup(title, summary, implementation, runtime).arrange(DOWN, buff=0.34)

        self.play(FadeIn(title), run_time=2.5)
        self.play(FadeIn(summary), run_time=5.0)
        self.play(FadeIn(implementation), FadeIn(runtime), run_time=4.0)
        self.wait(18)
        self.play(FadeOut(group), run_time=3.0)
