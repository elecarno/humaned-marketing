from manim import *
import numpy as np

class Main(Scene):
    def construct(self):
        # 1. Create a 2D axes centered on the screen
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True},
        )

        # 2. Add labels \hat{x} and \hat{y} near the axis tips
        x_label = MathTex(r"\hat{x}").next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = MathTex(r"\hat{y}").next_to(axes.y_axis.get_end(), UP, buff=0.2)
        labels = VGroup(x_label, y_label)

        # 3. Setup the Point at (2, 1) and its BLUE label \vec{a}
        point_coords = axes.c2p(2, 1)
        dot = Dot(point_coords, color=BLUE)
        a_label = MathTex(r"\vec{a}", color=BLUE).next_to(dot, UR, buff=0.15)

        # 4. Animate the axes and labels first
        self.play(Create(axes), Write(labels), run_time=1.5)
        self.wait(0.5)

        # 5. Draw the point and label AFTER axes are done
        self.play(FadeIn(dot, scale=0.5), Write(a_label))
        self.wait(1)

        # 6. Group all graphical elements together
        graph_group = VGroup(axes, labels, dot, a_label)

        # 7. Create the BLUE vector definition equation on the right
        eq1 = MathTex(
            r"\vec{a} = \begin{bmatrix} x_a \\ y_a \end{bmatrix} \in \mathbb{R}^{2}",
            color=BLUE
        ).scale(0.75)

        # 8. Shift graph left and reveal equation
        self.play(
            graph_group.animate.shift(LEFT * 2.7),
            run_time=1.5
        )
        
        # Position eq1 after shifting to ensure aligned layout
        eq1.to_edge(RIGHT, buff=3.6).to_edge(UP, buff=1.8)
        self.play(Write(eq1))
        self.wait(2)

        # =========================================================
        # SCRIPT: Translation degrees of freedom
        # =========================================================

        unit_x = axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]
        unit_y = axes.c2p(0, 1)[1] - axes.c2p(0, 0)[1]

        # Attach an updater so a_label follows the dot's position
        a_label.add_updater(lambda m: m.next_to(dot, UR, buff=0.15))

        # Shift right 1 unit along x-axis, then back
        self.play(dot.animate.shift(RIGHT * unit_x), run_time=1.0)
        self.play(dot.animate.shift(LEFT * unit_x), run_time=1.0)

        # Shift up 1 unit along y-axis, then back
        self.play(dot.animate.shift(UP * unit_y), run_time=1.0)
        self.play(dot.animate.shift(DOWN * unit_y), run_time=1.0)

        self.wait(1)

        # =========================================================
        # SCRIPT: Rotational degree of freedom
        # =========================================================

        axes_origin = axes.get_origin()

        # Rotate ONLY the dot around the origin
        self.play(
            Rotate(
                dot,
                angle=2 * PI,
                about_point=axes_origin,
                rate_func=smooth,
            ),
            run_time=3.0
        )

        a_label.clear_updaters()
        self.wait(1)

        # =========================================================
        # SCRIPT: General rotation definitions
        # =========================================================

        eq2 = MathTex(r"R \in \mathbb{R}^{2 \times 2}").scale(0.75).next_to(eq1, DOWN, aligned_edge=LEFT, buff=0.35)
        
        eq3 = MathTex(
            r"{\vec{b}}", r"=", r"R", r"{\vec{a}}", r"\in \mathbb{R}^{2}"
        ).scale(0.75).next_to(eq2, DOWN, aligned_edge=LEFT, buff=0.35)
        eq3.set_color_by_tex(r"{\vec{b}}", RED)
        eq3.set_color_by_tex(r"{\vec{a}}", BLUE)

        self.play(Write(eq2))
        self.wait(0.5)
        self.play(Write(eq3))
        self.wait(1)

        # Create point \vec{b} directly at \vec{a}'s position in RED
        dot_b = Dot(dot.get_center(), color=RED)
        b_label = MathTex(r"\vec{b}", color=RED).next_to(dot_b, UR, buff=0.15)

        # Keep b_label upright during rotation
        b_label.add_updater(lambda m: m.next_to(dot_b, UR, buff=0.15))

        # Fade in dot b over dot a
        self.play(FadeIn(dot_b, scale=0.5), Write(b_label))
        self.wait(0.5)

        # Rotate \vec{b} out from \vec{a} by 90 degrees
        self.play(
            Rotate(
                dot_b,
                angle=PI / 2,
                about_point=axes_origin,
                rate_func=smooth,
            ),
            run_time=2.0
        )

        b_label.clear_updaters()
        self.wait(2)

        # =========================================================
        # SWAP SCENE TO DEFINITION 
        # =========================================================

        self.play(
            FadeOut(graph_group),
            FadeOut(dot_b),
            FadeOut(b_label),
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(eq3),
            run_time=1.0
        )
        self.wait(0.5)

        title = Text("Special Orthogonal Group", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=1.2)

        line1 = Tex(
            r"The special orthogonal group is the set containing all rotation matrices and is denoted $\text{SO}(n)$."
        ).scale(0.75)

        line2 = Tex(
            r"It is the set of all matrices, $R\in \mathbb{R}^{n\times n}$, that satisfy the two conditions:"
        ).scale(0.75)

        text_block = VGroup(line1, line2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        text_block.next_to(title, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)

        conditions = MathTex(
            r"R^{T}R = I, \quad \det R = 1",
            color=YELLOW
        ).scale(0.85)

        conditions.next_to(text_block, DOWN, buff=0.75)
        conditions.alignment = "center"

        self.play(Write(title))
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=1.0)
        self.wait(0.5)
        self.play(Write(conditions), run_time=1.5)
        self.wait(3)

        # =========================================================
        # RETURN TO GRAPH SCENE AND INTRODUCE R(theta)
        # =========================================================

        def_scene_group = VGroup(title, line1, line2, conditions)
        self.play(FadeOut(def_scene_group), run_time=1.0)
        self.wait(0.3)

        self.play(
            FadeIn(graph_group),
            FadeIn(dot_b),
            FadeIn(b_label),
            FadeIn(eq1),
            FadeIn(eq2),
            FadeIn(eq3),
            run_time=1.0
        )
        self.wait(1.0)

        eq_theta = MathTex(
            r"\theta \in [0, 2\pi)"
        ).scale(0.75).next_to(eq1, DOWN, aligned_edge=LEFT, buff=0.35)

        eq2_theta = MathTex(
            r"R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \in \text{SO}(2)"
        ).scale(0.75).next_to(eq_theta, DOWN, aligned_edge=LEFT, buff=0.35)

        eq3_theta = MathTex(
            r"{\vec{b}}", r"=", r"R(\theta)", r"{\vec{a}}", r"\in \mathbb{R}^{2}"
        ).scale(0.75).next_to(eq2_theta, DOWN, aligned_edge=LEFT, buff=0.35)
        eq3_theta.set_color_by_tex(r"{\vec{b}}", RED)
        eq3_theta.set_color_by_tex(r"{\vec{a}}", BLUE)

        self.play(
            Write(eq_theta),
            TransformMatchingTex(eq2, eq2_theta),
            eq3.animate.next_to(eq2_theta, DOWN, aligned_edge=LEFT, buff=0.35),
            run_time=1.5
        )
        self.play(TransformMatchingTex(eq3, eq3_theta), run_time=1.2)
        
        self.play(Indicate(eq2_theta, scale_factor=1.1, color=YELLOW), run_time=1.2)
        self.wait(2)

        # =========================================================
        # DYNAMIC THETA ROTATION DEMONSTRATION (CLEAN & FAST)
        # =========================================================

        theta_tracker = ValueTracker(PI / 2)

        # Re-usable reference anchors
        ref_eq_theta_pos = eq_theta.get_corner(UL)
        ref_eq2_theta_pos = eq2_theta.get_corner(UL)
        ref_eq3_theta_pos = eq3_theta.get_corner(UL)

        # Define dynamic mobjects using always_redraw
        dyn_eq_theta = always_redraw(
            lambda: MathTex(
                rf"\theta = {theta_tracker.get_value():.2f} \in (0, 2\pi]"
            )
            .scale(0.75)
            .move_to(ref_eq_theta_pos, aligned_edge=UL)
        )

        dyn_eq2_theta = always_redraw(
            lambda: MathTex(
                rf"R({theta_tracker.get_value():.2f}) = \begin{{bmatrix}} {np.cos(theta_tracker.get_value()):.2f} & {-np.sin(theta_tracker.get_value()):.2f} \\ {np.sin(theta_tracker.get_value()):.2f} & {np.cos(theta_tracker.get_value()):.2f} \end{{bmatrix}} \in \text{{SO}}(2)"
            )
            .scale(0.75)
            .move_to(ref_eq2_theta_pos, aligned_edge=UL)
        )

        def make_dyn_eq3():
            val = theta_tracker.get_value()
            m = MathTex(
                r"{\vec{b}}", r"=", rf"R({val:.2f})", r"{\vec{a}}", r"\in \mathbb{R}^{2}"
            ).scale(0.75).move_to(ref_eq3_theta_pos, aligned_edge=UL)
            m.set_color_by_tex(r"{\vec{b}}", RED)
            m.set_color_by_tex(r"{\vec{a}}", BLUE)
            return m

        dyn_eq3_theta = always_redraw(make_dyn_eq3)

        # Replace static equations with the dynamic redrawers
        self.play(
            ReplacementTransform(eq_theta, dyn_eq_theta),
            ReplacementTransform(eq2_theta, dyn_eq2_theta),
            ReplacementTransform(eq3_theta, dyn_eq3_theta),
            run_time=0.5
        )

        # Update dot_b and b_label with the theta value
        def update_dot_b(m):
            val = theta_tracker.get_value()
            x_b = 2 * np.cos(val) - 1 * np.sin(val)
            y_b = 2 * np.sin(val) + 1 * np.cos(val)
            m.move_to(axes.c2p(x_b, y_b))

        dot_b.add_updater(update_dot_b)
        b_label.add_updater(lambda m: m.next_to(dot_b, UR, buff=0.15))

        # 1. Rotate counterclockwise (+ positive rotation)
        self.play(
            theta_tracker.animate.set_value(2.50),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # 2. Rotate clockwise (- negative rotation)
        self.play(
            theta_tracker.animate.set_value(-1.20),
            run_time=3.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # 3. Return rotation to theta = 1.00 rad
        self.play(
            theta_tracker.animate.set_value(PI / 2),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(2)

        # Clean up updaters
        dot_b.clear_updaters()
        b_label.clear_updaters()

        # =========================================================
        # REVERT DYNAMIC EQUATIONS BACK TO SYMBOLIC FORM
        # =========================================================

        # Clear always_redraw updaters from dynamic equations
        dyn_eq_theta.clear_updaters()
        dyn_eq2_theta.clear_updaters()
        dyn_eq3_theta.clear_updaters()

        # Re-create static symbolic equations positioned at the anchors
        final_eq_theta = MathTex(
            r"\theta \in [0, 2\pi)"
        ).scale(0.75).move_to(ref_eq_theta_pos, aligned_edge=UL)

        final_eq2_theta = MathTex(
            r"R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \in \text{SO}(2)"
        ).scale(0.75).move_to(ref_eq2_theta_pos, aligned_edge=UL)

        final_eq3_theta = MathTex(
            r"{\vec{b}}", r"=", r"R(\theta)", r"{\vec{a}}", r"\in \mathbb{R}^{2}"
        ).scale(0.75).move_to(ref_eq3_theta_pos, aligned_edge=UL)
        final_eq3_theta.set_color_by_tex(r"{\vec{b}}", RED)
        final_eq3_theta.set_color_by_tex(r"{\vec{a}}", BLUE)

        # Animate transition from dynamic numerical values back to symbolic variables
        self.play(
            ReplacementTransform(dyn_eq_theta, final_eq_theta),
            ReplacementTransform(dyn_eq2_theta, final_eq2_theta),
            ReplacementTransform(dyn_eq3_theta, final_eq3_theta),
            run_time=1.5
        )

        self.wait(2)