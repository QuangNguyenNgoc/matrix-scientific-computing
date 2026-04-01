# check_manim.py


def check_manim():
    from manim import Scene, Square

    print("[OK] Manim imported")

    # test object
    sq = Square()
    print("[OK] Square object created:", sq)


def check_latex():
    from manim import MathTex

    expr = MathTex(r"\int_0^1 x dx")
    print("[OK] LaTeX (MathTex) working")


def main():
    print("=== Checking Manim environment ===")
    check_manim()
    try:
        check_latex()
    except Exception as e:
        print("[WARN] LaTeX not working:", e)
    print("=== DONE ===")


if __name__ == "__main__":
    main()

# # EXPECT OUTPUT

# [OK] Manim imported
# [OK] Square object created
# [OK] LaTeX (MathTex) working
