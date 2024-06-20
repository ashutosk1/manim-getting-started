from manim import *
import numpy as np
import math

class SineSeries(Scene):
    def construct(self):
        
        # Title 
        title = Text("Maclaurin Series Expansion of sin(x)").scale(0.9).to_edge(DOWN)
        self.play(Write(title))


        x_range = [-5, 5]
        y_range = [-1, 1]
        ax = Axes(x_range=x_range, y_range=y_range)
        axes_labels = ax.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(ax), Write(axes_labels))


        # Get the equation of sinx
        curve = FunctionGraph(lambda x : np.sin(x))
        self.play(Create(curve))

        n = 9
        series_base = r"\sin(x) = "
        current_series = series_base
        series_expansion = MathTex(current_series).scale(0.4).to_corner(UL)
        self.wait(1)

        series_curve = curve.copy()
        for i in range(n):
            # Expression
            sign = "-" if i % 2 == 1 else "+"
            exponent = 2 * i + 1
            new_term = rf"{sign} \frac{{x^{{{exponent}}}}}{{{exponent}!}}"
            current_series += " " + new_term
            new_series_expansion = MathTex(current_series).scale(0.4).to_corner(UL)
            
            self.play(Transform(series_expansion, new_series_expansion))
            
            # Curve
            def updated_func(x, i=i):
                terms = [((-1)**k * x**(2*k + 1)) / math.factorial(2*k + 1) for k in range(i+1)]
                return sum(terms)
            
            updated_series_curve = FunctionGraph(lambda x : updated_func(x), color=RED)
            self.play(FadeOut(series_curve))
            self.play(Create(updated_series_curve))
            series_curve = updated_series_curve

        self.wait(2)
        