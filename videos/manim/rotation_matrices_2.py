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

        def create_3d_axes(with_subscript=False):
            axes = ThreeDAxes(
                x_range=[-4, 4, 1],
                y_range=[-4, 4, 1],
                z_range=[-4, 4, 1],
                x_length=7.0,
                y_length=7.0,
                z_length=6.0,
            )
            
            x_str = r"\hat{x}_{\mathrm{s}}" if with_subscript else r"\hat{x}"
            y_str = r"\hat{y}_{\mathrm{s}}" if with_subscript else r"\hat{y}"
            z_str = r"\hat{z}_{\mathrm{s}}" if with_subscript else r"\hat{z}"

            x_label = MathTex(x_str).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
            y_label = MathTex(y_str).next_to(axes.y_axis.get_end(), UP, buff=0.2)
            z_label = MathTex(z_str).next_to(axes.z_axis.get_end(), UP, buff=0.2)
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

        # Build initial 3D elements (Standard labels)
        axes1, labels1 = create_3d_axes(with_subscript=False)

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

        # ==========================================
        # SECTION 1: INTRODUCTION & SETUP
        # ==========================================
        self.next_section("Section 1: Intro & Setup", skip_animations=True)

        self.add_fixed_orientation_mobjects(*labels1)
        self.play(Create(axes1), Write(labels1), run_time=1.5)
        self.wait(0.5)

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

        # ==========================================
        # SECTION 2: ROTATION ABOUT X-AXIS
        # ==========================================
        self.next_section("Section 2: Rotation about X-Axis", skip_animations=True)

        self.play(
            Unwrite(title),
            Unwrite(rx_mat),
            Unwrite(ry_mat),
            Unwrite(rz_mat),
            run_time=1.0
        )
        self.wait(0.3)

        axes2, labels2 = create_3d_axes(with_subscript=False)
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

        theta_tracker = ValueTracker(0)

        def clean_str(val):
            val = 0.0 if abs(val) < 1e-4 else val
            return f"{val:+.2f}"

        dynamic_theta = always_redraw(lambda: MathTex(
            rf"\theta = {theta_tracker.get_value():.2f} \in \mathbb{{R}}"
        ).scale(0.75).next_to(eq1_p2, DOWN, aligned_edge=LEFT, buff=0.35))

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

        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6.0,
            rate_func=linear
        )

        dot_a2.remove_updater(update_dot)
        projections2.remove_updater(update_projections)
        self.wait(2)

        # ==========================================
        # SECTION 3: ROTATION ABOUT Y-AXIS
        # ==========================================
        self.next_section("Section 3: Rotation about Y-Axis", skip_animations=True)
        
        theta_tracker.set_value(0)

        dynamic_Ry = always_redraw(lambda: MathTex(
            rf"R_{{y}}({theta_tracker.get_value():.2f}) = \begin{{bmatrix}}"
            rf"{clean_str(np.cos(theta_tracker.get_value()))} & 0 & {clean_str(np.sin(theta_tracker.get_value()))} \\"
            rf"0 & 1 & 0 \\"
            rf"{clean_str(-np.sin(theta_tracker.get_value()))} & 0 & {clean_str(np.cos(theta_tracker.get_value()))}"
            r"\end{bmatrix}"
        ).scale(0.65).next_to(dynamic_theta, DOWN, aligned_edge=LEFT, buff=0.35))

        self.add_fixed_in_frame_mobjects(dynamic_Ry)

        self.play(
            ReplacementTransform(dynamic_Rx, dynamic_Ry),
            run_time=1.0
        )
        self.wait(0.5)

        def update_dot_y(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0] * c + initial_p[2] * s,
                initial_p[1],
                -initial_p[0] * s + initial_p[2] * c
            ])
            m.move_to(axes2.c2p(*curr_p))

        def update_projections_y(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0] * c + initial_p[2] * s,
                initial_p[1],
                -initial_p[0] * s + initial_p[2] * c
            ])
            m.become(get_projections(axes2, curr_p))

        dot_a2.add_updater(update_dot_y)
        projections2.add_updater(update_projections_y)

        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6.0,
            rate_func=linear
        )

        dot_a2.remove_updater(update_dot_y)
        projections2.remove_updater(update_projections_y)
        self.wait(2)

        # ==========================================
        # SECTION 4: ROTATION ABOUT Z-AXIS
        # ==========================================
        self.next_section("Section 4: Rotation about Z-Axis", skip_animations=True)
        
        theta_tracker.set_value(0)

        dynamic_Rz = always_redraw(lambda: MathTex(
            rf"R_{{z}}({theta_tracker.get_value():.2f}) = \begin{{bmatrix}}"
            rf"{clean_str(np.cos(theta_tracker.get_value()))} & {clean_str(-np.sin(theta_tracker.get_value()))} & 0 \\"
            rf"{clean_str(np.sin(theta_tracker.get_value()))} & {clean_str(np.cos(theta_tracker.get_value()))} & 0 \\"
            rf"0 & 0 & 1"
            r"\end{bmatrix}"
        ).scale(0.65).next_to(dynamic_theta, DOWN, aligned_edge=LEFT, buff=0.35))

        self.add_fixed_in_frame_mobjects(dynamic_Rz)

        self.play(
            ReplacementTransform(dynamic_Ry, dynamic_Rz),
            run_time=1.0
        )
        self.wait(0.5)

        def update_dot_z(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0] * c - initial_p[1] * s,
                initial_p[0] * s + initial_p[1] * c,
                initial_p[2]
            ])
            m.move_to(axes2.c2p(*curr_p))

        def update_projections_z(m):
            t = theta_tracker.get_value()
            c, s = np.cos(t), np.sin(t)
            curr_p = np.array([
                initial_p[0] * c - initial_p[1] * s,
                initial_p[0] * s + initial_p[1] * c,
                initial_p[2]
            ])
            m.become(get_projections(axes2, curr_p))

        dot_a2.add_updater(update_dot_z)
        projections2.add_updater(update_projections_z)

        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6.0,
            rate_func=linear
        )

        dot_a2.remove_updater(update_dot_z)
        projections2.remove_updater(update_projections_z)
        self.wait(2)

        # ==========================================
        # SECTION 5: INTRODUCE SPACE FRAME {s}
        # ==========================================
        self.next_section("Section 5: Space Frame Intro", skip_animations=False)

        self.play(
            FadeOut(dot_a2),
            Unwrite(a_label2),
            Uncreate(projections2),
            Unwrite(eq1_p2),
            Unwrite(dynamic_theta),
            Unwrite(dynamic_Rz),
            run_time=1.2
        )
        self.wait(0.5)

        # Create labels with 's' subscript
        _, s_labels = create_3d_axes(with_subscript=True)
        self.add_fixed_orientation_mobjects(*s_labels)

        space_frame_label = MathTex(r"\{\mathrm{s}\}", color=WHITE).scale(0.85)
        space_frame_label.move_to(axes2.c2p(0, 0, 0) + LEFT * 0.5 + DOWN * 0.5 + OUT * 1.0)

        self.add_fixed_orientation_mobjects(space_frame_label)

        # Transform standard axis labels into space-frame axis labels
        self.play(
            Transform(labels2, s_labels),
            Write(space_frame_label),
            run_time=1.2
        )
        self.wait(2)

        ## ==========================================
        # SECTION 6: INTRODUCE BODY FRAME {b}
        # ==========================================
        self.next_section("Section 6: Body Frame Intro", skip_animations=False)

        # Origin point of the body frame in space coordinates
        body_origin_coords = np.array([1.0, 1.0, 2.0])
        body_origin_p = axes2.c2p(*body_origin_coords)

        # Create dashed projection lines connecting frame {s} origin to frame {b} origin
        body_projections = get_projections(axes2, body_origin_coords)

        # Length of unit axis vectors for the body frame
        axis_length = 1.0

        # Define 3D unit arrows originating from (1, 1, 2)
        x_b_arrow = Arrow3D(
            start=body_origin_p,
            end=axes2.c2p(*(body_origin_coords + np.array([axis_length, 0, 0]))),
            color=RED,
            thickness=0.02
        )
        y_b_arrow = Arrow3D(
            start=body_origin_p,
            end=axes2.c2p(*(body_origin_coords + np.array([0, axis_length, 0]))),
            color=GREEN,
            thickness=0.02
        )
        z_b_arrow = Arrow3D(
            start=body_origin_p,
            end=axes2.c2p(*(body_origin_coords + np.array([0, 0, axis_length]))),
            color=BLUE,
            thickness=0.02
        )

        body_axes = VGroup(x_b_arrow, y_b_arrow, z_b_arrow)

        # Labels for the body frame axes and frame identifier
        x_b_label = MathTex(r"\hat{x}_{\mathrm{b}}", color=RED).next_to(x_b_arrow.get_end(), RIGHT, buff=0.15)
        y_b_label = MathTex(r"\hat{y}_{\mathrm{b}}", color=GREEN).next_to(y_b_arrow.get_end(), UP, buff=0.15)
        z_b_label = MathTex(r"\hat{z}_{\mathrm{b}}", color=BLUE).next_to(z_b_arrow.get_end(), UP, buff=0.15)

        body_frame_label = MathTex(r"\{\mathrm{b}\}", color=YELLOW).scale(0.85)
        body_frame_label.move_to(body_origin_p + LEFT * 0.45 + DOWN * 0.35)

        body_labels = VGroup(x_b_label, y_b_label, z_b_label, body_frame_label)

        # Keep 2D labels facing the camera in 3D scene
        self.add_fixed_orientation_mobjects(*body_labels)

        # Animate creation of body frame and projection lines simultaneously
        self.play(
            Create(body_projections),
            Create(body_axes),
            Write(body_labels),
            run_time=1.5
        )
        self.wait(2)

        # ==========================================
        # SECTION 7: ANGULAR VELOCITY / ROTATION
        # ==========================================
        self.next_section("Section 7: Body Frame Rotation", skip_animations=False)

        # 1. Tracker for continuous rotation angle
        rot_tracker = ValueTracker(0)

        # Base radius and z-height for origin trajectory
        # Initial origin is at (1, 1, 2) -> r = sqrt(2), initial angle = pi/4
        r_orig = np.sqrt(1.0**2 + 1.0**2)
        initial_phi = np.pi / 4  # atan2(1, 1)
        z_orig = 2.0

        # Helper function to compute rotated origin in {s} coordinates
        def get_rotated_origin(angle):
            phi = initial_phi + angle
            return np.array([
                r_orig * np.cos(phi),
                r_orig * np.sin(phi),
                z_orig
            ])

        # Helper function to compute rotated unit vector axes
        def get_rotated_axes(angle):
            c, s = np.cos(angle), np.sin(angle)
            R_z = np.array([
                [c, -s, 0],
                [s,  c, 0],
                [0,  0, 1]
            ])
            x_dir = R_z @ np.array([1, 0, 0])
            y_dir = R_z @ np.array([0, 1, 0])
            z_dir = R_z @ np.array([0, 0, 1])
            return x_dir, y_dir, z_dir

        # 2. Add \theta(t) to the 2D screen overlay on the right side
        theta_var = MathTex(r"\theta(t)", color=YELLOW).scale(0.75)
        
        # Register as a 2D fixed-in-frame mobject FIRST
        self.add_fixed_in_frame_mobjects(theta_var)
        
        # Position on the right edge (aligned with your earlier equations layout)
        theta_var.to_edge(RIGHT, buff=1.8).to_edge(UP, buff=1.8)

        # 3. Dynamic projection lines that follow the rotating frame
        dynamic_projections = always_redraw(
            lambda: get_projections(axes2, get_rotated_origin(rot_tracker.get_value()))
        )

        # 4. Dynamic 3D Arrows for frame {b}
        def create_dynamic_body_axes():
            angle = rot_tracker.get_value()
            orig = get_rotated_origin(angle)
            orig_p = axes2.c2p(*orig)
            
            x_dir, y_dir, z_dir = get_rotated_axes(angle)
            
            x_arr = Arrow3D(
                start=orig_p,
                end=axes2.c2p(*(orig + x_dir * axis_length)),
                color=RED,
                thickness=0.02
            )
            y_arr = Arrow3D(
                start=orig_p,
                end=axes2.c2p(*(orig + y_dir * axis_length)),
                color=GREEN,
                thickness=0.02
            )
            z_arr = Arrow3D(
                start=orig_p,
                end=axes2.c2p(*(orig + z_dir * axis_length)),
                color=BLUE,
                thickness=0.02
            )
            return VGroup(x_arr, y_arr, z_arr)

        dynamic_body_axes = always_redraw(create_dynamic_body_axes)

        # 5. Dynamic text labels following moving frame {b}
        dynamic_x_label = always_redraw(lambda: MathTex(r"\hat{x}_{\mathrm{b}}", color=RED).next_to(
            axes2.c2p(*(get_rotated_origin(rot_tracker.get_value()) + get_rotated_axes(rot_tracker.get_value())[0] * axis_length)),
            RIGHT, buff=0.15
        ))
        dynamic_y_label = always_redraw(lambda: MathTex(r"\hat{y}_{\mathrm{b}}", color=GREEN).next_to(
            axes2.c2p(*(get_rotated_origin(rot_tracker.get_value()) + get_rotated_axes(rot_tracker.get_value())[1] * axis_length)),
            UP, buff=0.15
        ))
        dynamic_z_label = always_redraw(lambda: MathTex(r"\hat{z}_{\mathrm{b}}", color=BLUE).next_to(
            axes2.c2p(*(get_rotated_origin(rot_tracker.get_value()) + get_rotated_axes(rot_tracker.get_value())[2] * axis_length)),
            UP, buff=0.15
        ))
        dynamic_b_label = always_redraw(lambda: MathTex(r"\{\mathrm{b}\}", color=YELLOW).scale(0.85).move_to(
            axes2.c2p(*get_rotated_origin(rot_tracker.get_value())) + LEFT * 0.45 + DOWN * 0.35
        ))

        dynamic_labels = VGroup(dynamic_x_label, dynamic_y_label, dynamic_z_label, dynamic_b_label)
        self.add_fixed_orientation_mobjects(*dynamic_labels)

        # Swap static elements out for dynamic elements
        self.remove(body_axes, body_labels, body_projections)
        self.add(dynamic_body_axes, dynamic_labels, dynamic_projections)

        # Animate \theta(t) onto the 2D panel on the right
        self.play(Write(theta_var), run_time=0.8)

        # 6. Continuous rotation animation around z_s axis
        self.play(
            rot_tracker.animate.set_value(2 * PI),
            run_time=8.0,
            rate_func=linear
        )

        self.wait(2)