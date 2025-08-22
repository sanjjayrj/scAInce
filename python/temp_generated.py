from manim import *

class QuadraticFormulaVisualization(Scene):
    def construct(self):
        axes = Axes(x_range=[-10, 10, 1], y_range=[-10, 10, 1], axis_config={"include_numbers": True})
        quadratic_graph = axes.plot(lambda x: x**2 - 4*x + 3, color=BLUE)
        roots = [-1, 3]
        root_dots = [Dot(axes.coords_to_point(x, 0), color=RED) for x in roots]
        labels = VGroup(
            MathTex("x = 1").next_to(root_dots[0], DOWN),
            MathTex("x = 3").next_to(root_dots[1], DOWN)
        )

        equation = MathTex("x^2 - 4x + 3 = 0").to_edge(UP)
        
        self.add(axes, quadratic_graph, equation)
        self.play(*[FadeIn(dot) for dot in root_dots])
        self.play(*[Write(label) for label in labels])