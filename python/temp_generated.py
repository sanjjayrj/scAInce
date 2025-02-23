from manim import *

class SineWave(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        )

        sine_wave = axes.plot(lambda x: np.sin(x), color=YELLOW)
        self.add(axes, sine_wave)
        self.play(Create(sine_wave), run_time=4)