from manim import *

class PiezoelectricEffect(Scene):
    def construct(self):
        crystal = Rectangle(width=4, height=2, color=BLUE).shift(LEFT*3)
        arrows = VGroup(
            Arrow(start=LEFT, end=RIGHT, color=YELLOW).shift(UP*0.5),
            Arrow(start=LEFT, end=RIGHT, color=YELLOW).shift(DOWN*0.5)
        ).shift(RIGHT*3)
        
        self.play(FadeIn(crystal))
        self.wait(1)
        self.play(crystal.animate.shift(RIGHT*6).set_color(RED), run_time=2)
        self.play(FadeIn(arrows))
        self.wait(2)