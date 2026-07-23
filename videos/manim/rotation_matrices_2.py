import numpy as np
from manim import *

class RotationMatrices2(ThreeDScene):
    def construct(self):
        # 1. Camera setup
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            gamma=0 * DEGREES,
            frame_center=[1.8, 0.4, 0]
        )

        def create_3d_axes():
            axes = ThreeDAxes(
                x_range=[-4, 4, 1],
                y_range=[-4, 4, 1],
                z_range=[-4, 4, 1],
                x_length=7.0,
                y_length=7.0,
                z_length=6.0,
            )
            x_label = MathTex(r"\hat{x}").next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
            y_label = MathTex(r"\hat{y}").next_to(axes.y_axis.get_end(), UP, buff=0.2)
            z_label = MathTex(r"\hat{z}").next_to(axes.z_axis.get_end(), UP, buff=0.2)
            labels = VGroup(x_label, y_label, z_label)
            return axes, labels

        def get_projections(axes, p):
            p_curr = axes.c2p(*p)
            p_xy = axes.c2p(p[0], p[1], 0)
            p_x  = axes.c2p(p[0], 0, 0)
            p_y  = axes.c2p(0, p[1], 0)

            line_z = DashedLine(p_curr, p_xy, color=BLUE_B, stroke_width=2)
            line_x = DashedLine(p_xy, p_x, color=GRAY, stroke_width=2)
            line_y = DashedLine(p_xy, p_y, color=GRAY, stroke_width=2)
            return VGroup(line_z, line_x, line_y)

        # Build initial 3D elements
        axes1, labels1 = create_3d_axes()

        initial_p = np.array([1.0, 1.0, 2.0])
        dot_a1 = Dot3D(axes1.c2p(*initial_p), color=BLUE)
        
        a_label1 = MathTex(r"\vec{a}", color=BLUE)
        a_label1.add_updater(lambda m: m.next_to(dot_a1, UR, buff=0.15))

        projections1 = get_projections(axes1, initial_p)

        # Equations for Part 1
        eq1 = MathTex(
            r"\vec{a} = \begin{bmatrix} x_a \\ y_a \\ z_a \end{bmatrix} \in \mathbb{R}^{3}",
            color=BLUE
        ).scale(0.75).to_edge(RIGHT, buff=1.2).to_edge(UP, buff=1.8)

        eq_theta = MathTex(r"\theta \in \mathbb{R}").scale(0.75).next_to(eq1, DOWN, aligned_edge=LEFT, buff=0.35)
        eq_R = MathTex(r"R(\theta) \in \text{SO}(3)").scale(0.75).next_to(eq_theta, DOWN, aligned_edge=LEFT, buff=0.35)

        # --- ANIMATIONS: PART 1 ---
        self.add_fixed_orientation_mobjects(*labels1)
        self.play(Create(axes1), Write(labels1), run_time=1.5)
        self.wait(0.5)

        # Lock UI elements to 2D frame only right when introduced
        self.add_fixed_orientation_mobjects(a_label1)
        self.add_fixed_in_frame_mobjects(eq1)

        self.play(
            FadeIn(dot_a1, scale=0.5), 
            Write(a_label1),
            Create(projections1),
            Write(eq1),
            run_time=1.5
        )
        self.wait(1.5)

        self.add_fixed_in_frame_mobjects(eq_theta)
        self.play(Write(eq_theta))
        self.wait(0.5)
        
        self.add_fixed_in_frame_mobjects(eq_R)
        self.play(Write(eq_R))
        self.wait(2)

        # --- CUT TO ELEMENTARY ROTATION MATRICES ---
        self.play(
            Uncreate(axes1),
            Unwrite(labels1),
            FadeOut(dot_a1),
            Unwrite(a_label1),
            Uncreate(projections1),
            Unwrite(eq1),
            Unwrite(eq_theta),
            Unwrite(eq_R),
            run_time=1.2
        )
        self.wait(0.5)

        title = Text("Elementary Rotations", font_size=36, weight=BOLD).to_edge(UP, buff=0.8).shift(RIGHT * 1.53)

        rx_mat = MathTex(r"R_{x}(\theta) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix}").scale(0.7)
        ry_mat = MathTex(r"R_{y}(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}").scale(0.7)
        rz_mat = MathTex(r"R_{z}(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}").scale(0.7)

        VGroup(rx_mat, ry_mat, rz_mat).arrange(DOWN, buff=0.45).next_to(title, DOWN, buff=0.6).shift(RIGHT * 0.38)

        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(0.3)

        for mat in [rx_mat, ry_mat, rz_mat]:
            self.add_fixed_in_frame_mobjects(mat)
            self.play(Write(mat), run_time=0.8)
            self.wait(0.2)

        self.wait(1.5)

        # --- PART 2: RETURN TO 3D SCENE & ROTATE ABOUT X-AXIS ---
        self.play(
            Unwrite(title),
            Unwrite(rx_mat),
            Unwrite(ry_mat),
            Unwrite(rz_mat),
            run_time=1.0
        )
        self.wait(0.3)

        axes2, labels2 = create_3d_axes()
        dot_a2 = Dot3D(axes2.c2p(*initial_p), color=BLUE)
        
        a_label2 = MathTex(r"\vec{a}", color=BLUE)
        a_label2.add_updater(lambda m: m.next_to(dot_a2, UR, buff=0.15))

        eq1_p2 = MathTex(
            r"\vec{a} = \begin{bmatrix} x_a \\ y_a \\ z_a \end{bmatrix} \in \mathbb{R}^{3}",
            color=BLUE
        ).scale(0.75).to_edge(RIGHT, buff=1.2).to_edge(UP, buff=1.8)

        eq_theta_static = MathTex(r"\theta = 0.00 \in \mathbb{R}").scale(0.75).next_to(eq1_p2, DOWN, aligned_edge=LEFT, buff=0.35)

        eq_Rx_static = MathTex(
            r"R_{x}(0.00) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix}"
        ).scale(0.65).next_to(eq_theta_static, DOWN, aligned_edge=LEFT, buff=0.35)

        projections2 = get_projections(axes2, initial_p)

        # Lock Part 2 elements to frame right before animating
        self.add_fixed_orientation_mobjects(*labels2, a_label2)
        self.add_fixed_in_frame_mobjects(eq1_p2, eq_theta_static, eq_Rx_static)

        self.play(
            Create(axes2), 
            Write(labels2), 
            FadeIn(dot_a2, scale=0.5),
            Write(a_label2),
            Create(projections2),
            Write(eq1_p2),
            Write(eq_theta_static),
            Write(eq_Rx_static),
            run_time=1.2
        )
        self.wait(1)

        # --- DYNAMIC LATEX MATRIX & THETA DEFINITION ---
        theta_tracker = ValueTracker(0)

        def clean_str(val):
            val = 0.0 if abs(val) < 1e-4 else val
            return f"{val:+.2f}"

        # Dynamic \theta equation
        dynamic_theta = always_redraw(lambda: MathTex(
            rf"\theta = {theta_tracker.get_value():.2f} \in \mathbb{{R}}"
        ).scale(0.75).next_to(eq1_p2, DOWN, aligned_edge=LEFT, buff=0.35))

        # Dynamic matrix equation with live theta value inside R_x(...)
        dynamic_Rx = always_redraw(lambda: MathTex(
            rf"R_{{x}}({theta_tracker.get_value():.2f}) = \begin{{bmatrix}}"
            rf"1 & 0 & 0 \\"
            rf"0 & {clean_str(np.cos(theta_tracker.get_value()))} & {clean_str(-np.sin(theta_tracker.get_value()))} \\"
            rf"0 & {clean_str(np.sin(theta_tracker.get_value()))} & {clean_str(np.cos(theta_tracker.get_value()))}"
            r"\end{bmatrix}"
        ).scale(0.65).next_to(dynamic_theta, DOWN, aligned_edge=LEFT, buff=0.35))

        self.add_fixed_in_frame_mobjects(dynamic_theta, dynamic_Rx)

        self.play(
            ReplacementTransform(eq_theta_static, dynamic_theta),
            ReplacementTransform(eq_Rx_static, dynamic_Rx),
            run_time=0.5
        )
        self.wait(0.5)

        # 3D Point and Projection Updaters
        def update_dot(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0],
                initial_p[1] * c - initial_p[2] * s,
                initial_p[1] * s + initial_p[2] * c
            ])
            m.move_to(axes2.c2p(*curr_p))

        def update_projections(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0],
                initial_p[1] * c - initial_p[2] * s,
                initial_p[1] * s + initial_p[2] * c
            ])
            m.become(get_projections(axes2, curr_p))

        dot_a2.add_updater(update_dot)
        projections2.add_updater(update_projections)

        # Animate full rotation
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6.0,
            rate_func=linear
        )

        dot_a2.remove_updater(update_dot)
        projections2.remove_updater(update_projections)
        self.wait(2)