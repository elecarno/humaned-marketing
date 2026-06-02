from manim import *

class Mechanism2R(Scene):
    def construct(self):
        # show links
        line_L1 = Line(LEFT*2, RIGHT*2, stroke_width=10)
        line_L2 = Line(LEFT*2, RIGHT*2, stroke_width=10)
        group_links = VGroup(line_L1, line_L2).arrange(RIGHT, buff=1)

        lab_L1 = MathTex("\\L_{1}")
        lab_L2 = MathTex("\\L_{2}")
        lab_L1.add_updater(lambda m: m.next_to(line_L1, UP*1.5))
        lab_L2.add_updater(lambda m: m.next_to(line_L2, UP*1.5))

        lab_links = Text("Links").shift(DOWN * 1.5)

        self.play(
            Create(line_L1),
            Create(line_L2),
        )
        self.play(
            Write(lab_links), 
            Write(lab_L1), 
            Write(lab_L2)
        )
        self.wait(0.5)

        # show joints
        circ_J1 = Circle(0.5, stroke_color=WHITE, color=BLACK, fill_opacity=1.0)
        circ_J2 = Circle(0.5, stroke_color=WHITE, color=BLACK, fill_opacity=1.0)
        group_joints = VGroup(
            circ_J1, circ_J2
        ).arrange(RIGHT, buff=4).shift(UP*2)

        lab_J1 = MathTex("\\theta_{1}")
        lab_J2 = MathTex("\\theta_{2}")
        lab_J1.add_updater(lambda m: m.move_to(circ_J1.get_center()))
        lab_J2.add_updater(lambda m: m.move_to(circ_J2.get_center()))

        lab_links_and_joints = Text("Links & Joints").shift(DOWN * 1.5)

        self.play(
            Create(circ_J1),
            Create(circ_J2),
        )
        self.play(
            Write(lab_J1),
            Write(lab_J2),
            Transform(lab_links, lab_links_and_joints)
        )

        self.wait(1)

        # rearrange links and joints into a 2R robot
        self.play(Unwrite(lab_links))

        shift_vector_L2 = line_L1.get_end() - line_L2.get_start()

        self.play(
            line_L2.animate.shift(shift_vector_L2)
        )
        self.play(
            circ_J1.animate.move_to(line_L1.get_start()),
            circ_J2.animate.move_to(line_L2.get_start())
        )

        group_2R = VGroup(
            line_L1, line_L2, circ_J1, circ_J2,
            lab_L1, lab_L2, lab_J1, lab_J2
        )
        
        self.play(
            group_2R.animate.scale(0.7)
        )
        
        self.wait(1)