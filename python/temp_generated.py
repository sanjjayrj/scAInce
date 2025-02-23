from manim import *

class BallRollingDownHill(Scene):
    def construct(self):
        ground = Line(LEFT * 4, RIGHT * 4)
        hill = Line(LEFT * 4, RIGHT * 2 + DOWN * 2)
        ball = Dot(color=RED).shift(LEFT * 4 + UP * 0.1)

        self.add(ground, hill, ball)
        self.play(ball.animate.move_to(RIGHT * 2 + DOWN * 2.1), run_time=3, rate_func=rate_functions.ease_in_quad)