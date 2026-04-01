# test_render.py
from manim import *


class TestScene(Scene):
    def construct(self):
        text = Text("Hello Manim")
        self.play(Write(text))
        self.wait(1)


# RUN: manim test_render.py TestScene -pqh
# -> video sẽ bật lên
