from manim import *
import numpy as np
import math

class PythagoreanTheorem(Scene):
    def construct(self):
        # Title 
        title = Text("Pythagorean Theorem Proof").scale(0.9).to_edge(UP)
        self.play(Write(title))

        # Set-up Triangle
        A = 0.5 * np.array([-1, -1, 0])
        B = 0.5 * np.array([3, -1, 0])
        C = 0.5 * np.array([-1, 2, 0])

        # Create Triangle
        triangle = Polygon(A, B, C, color=BLUE)
        self.play(Create(triangle))

        # Labels
        label_A = Tex("A").next_to(A, DL)
        label_B = Tex("B").next_to(B, RIGHT)
        label_C = Tex("C").next_to(C, UP)
        self.play(Write(label_A), Write(label_B), Write(label_C))

        # Sides and Squares
        side_ab = np.linalg.norm(A - B)
        side_bc = np.linalg.norm(B - C)
        side_ca = np.linalg.norm(C - A)

        square_b = Square(side_length=side_ca, color=BLUE, fill_opacity=0.5).move_to(A + 0.5 * (C - A) + 0.5 * LEFT * side_ca)
        square_c = Square(side_length=side_ab, color=RED, fill_opacity=0.5).move_to(B + 0.5 * (A - B) + 0.5 * DOWN * side_ab)

        direction = C - B
        unit_direction = direction / side_bc
        perpendicular = np.array([unit_direction[1], -unit_direction[0], 0])
        dot_C_ext = C + side_bc * perpendicular
        dot_B_ext = B + side_bc * perpendicular
        square_a = Polygon(B, C, dot_C_ext, dot_B_ext, color=GREEN, fill_opacity=0.5)

        # Labels for Areas
        label_area_a = MathTex(r"a^2").move_to(square_a.get_center())
        label_area_b = MathTex(r"b^2").move_to(square_b.get_center())
        label_area_c = MathTex(r"c^2").move_to(square_c.get_center())

        self.play(Create(square_a), Create(square_b), Create(square_c))
        self.play(Write(label_area_a), Write(label_area_b), Write(label_area_c))
        self.wait(3)

        # Moving square_c into square_a
        angle_of_rotation = PI/2 - math.atan(side_ca / side_ab)
        square_c_copy = square_c.copy()
        self.play(Rotate(square_c_copy, angle=angle_of_rotation))
        self.play(square_c_copy.animate.move_to(B + 0.5 * side_ab * unit_direction + 0.5 * side_ab * perpendicular))

        # Shading areas in square_b
        offset_a_c = side_bc - side_ab
        offset_a_b = side_bc - side_ca
        
        # Get the vertices for the shaded regions
        shaded_vertices_1 = [
            square_b.get_corner(UR),
            square_b.get_corner(UR) + LEFT * offset_a_c,
            square_b.get_corner(DR) + LEFT * offset_a_c,
            square_b.get_corner(DR)
        ]
        shaded_vertices_2 = [
            square_b.get_corner(UR) + LEFT * offset_a_c,
            square_b.get_corner(UR) + 2 * LEFT * offset_a_c,
            square_b.get_corner(DR) + 2 * LEFT * offset_a_c,
            square_b.get_corner(DR) + LEFT * offset_a_c
        ]
        shaded_vertices_3 = [
            square_b.get_corner(UR) + 2 * LEFT * offset_a_c,
            square_b.get_corner(UL),
            square_b.get_corner(UL) + DOWN * offset_a_b,
            square_b.get_corner(UR) + 2 * LEFT * offset_a_c + DOWN * offset_a_b
        ]

        shaded_area_1 = Polygon(*shaded_vertices_1, color=BLUE, fill_opacity=0.5)
        shaded_area_2 = Polygon(*shaded_vertices_2, color=BLUE, fill_opacity=0.5)
        shaded_area_3 = Polygon(*shaded_vertices_3, color=BLUE, fill_opacity=0.5)
        combined_area = Union(shaded_area_1, shaded_area_2, shaded_area_3)
        shaded_area_4 = Difference(square_b, combined_area, color=BLUE, fill_opacity=0.5)

        self.play(Create(shaded_area_1), Create(shaded_area_2), Create(shaded_area_3), Create(shaded_area_4))

        # Move shaded areas into square_a
        self.play(Rotate(shaded_area_1, angle=PI/2 + angle_of_rotation))
        self.play(shaded_area_1.animate.move_to(C - 0.5 * offset_a_c * unit_direction + 0.5 * side_ca * perpendicular))

        self.play(Rotate(shaded_area_2, angle=PI + angle_of_rotation))
        self.play(shaded_area_2.animate.move_to(B + perpendicular*(side_ab + 0.5 * offset_a_c) + 0.5 * side_ca * unit_direction))

        self.play(Rotate(shaded_area_3, angle=PI/2 + angle_of_rotation))
        self.play(shaded_area_3.animate.move_to(C - 0.5 * offset_a_c * unit_direction + perpendicular*(side_ca + 0.5 * offset_a_b)))

        self.play(Rotate(shaded_area_4, angle=PI + angle_of_rotation))
        self.play(shaded_area_4.animate.move_to(B + perpendicular*(side_ab + 0.5 * offset_a_c)+ unit_direction*(side_ca + 0.5 *(side_ab - side_ca))))

        conclusion = MathTex(r"\text{Thus, } a^2 = b^2 + c^2").scale(0.8).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(3)