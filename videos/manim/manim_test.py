from manim import *

class Test(Scene):
    def construct(self):
        c = Circle(2, color = RED, fill_opacity = 0.1)

        self.play(DrawBorderThenFill(c), run_time = 0.5)

        title = Text("Manim Wahoo!", font_size=72, slant = "ITALIC").shift(UP * 0.3)
        subtitle = Text("Basics", slant = "ITALIC").shift(DOWN * 0.5)
        self.play(Write(title), Write(subtitle))

        self.wait(3)