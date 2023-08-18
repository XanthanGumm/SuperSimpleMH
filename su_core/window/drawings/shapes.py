import math
import pyMeow as pm
from su_core.math import CSharpVector2, CSharpMatrix3X2
from su_core.window.drawings import pm_colors


class Arrow:
    def __init__(self, start, end, short_render, text: str, color: str, start_pad):
        head_scalar: int = 15

        # head vertices - the size of the head
        head_v1 = CSharpVector2(-0.6, 0.0) * head_scalar  # left vertex
        head_v2 = CSharpVector2(0.0, math.sqrt(3) / 2) * head_scalar  # middle vertex
        head_v3 = CSharpVector2(0.6, 0.0) * head_scalar  # right vertex

        x_len = end.x - start.x
        y_len = end.y - start.y

        rot_angle = math.atan2(x_len, y_len)

        # add padding from the starting point
        start = start.rotate(rot_angle)
        start.y += start_pad
        start = start.rotate(-rot_angle)

        # add padding from the ending point
        end = end.rotate(rot_angle)
        end.y -= 5
        end = end.rotate(-rot_angle)

        head_v1 = head_v1.rotate(-rot_angle) + end
        head_v2 = head_v2.rotate(-rot_angle) + end
        head_v3 = head_v3.rotate(-rot_angle) + end

        # add 3 pixels padding from the head
        end = end.rotate(rot_angle)
        end.y -= 3
        end = end.rotate(-rot_angle)

        if not short_render:
            pm.draw_line(
                start.x, start.y, end.x, end.y, color=pm_colors[color], thick=2.0
            )

        pm.draw_text(
            text=text,
            posX=head_v3.x + 20,
            posY=head_v2.y - 5,
            fontSize=9,
            color=pm_colors["orange"],
        )
        pm.draw_triangle(
            head_v1.x,
            head_v1.y,
            head_v2.x,
            head_v2.y,
            head_v3.x,
            head_v3.y,
            color=pm_colors[color],
        )


class Cross:
    a, b, c, d = 0.25, 0.5, 0.75, 1.0
    points = (
        CSharpVector2(0, a),
        CSharpVector2(a, 0),
        CSharpVector2(b, a),
        CSharpVector2(c, 0),
        CSharpVector2(d, a),
        CSharpVector2(c, b),
        CSharpVector2(d, c),
        CSharpVector2(c, d),
        CSharpVector2(b, c),
        CSharpVector2(a, d),
        CSharpVector2(0, c),
        CSharpVector2(a, b),
        CSharpVector2(0, a),
    )

    def __init__(self, position, size, scale_x, scale_y, cross_color):
        for p in range(1, 13):
            start_point = position + (
                self.points[p - 1].multiply(size, size)
                - CSharpVector2(size / 2, size / 2)
            ).multiply(scale_x, scale_y)
            end_point = position + (
                self.points[p].multiply(size, size) - CSharpVector2(size / 2, size / 2)
            ).multiply(scale_x, scale_y)

            if len(cross_color) == 0:
                pm.draw_line(
                    start_point.x,
                    start_point.y,
                    end_point.x,
                    end_point.y,
                    color=pm_colors["white"],
                    thick=1,
                )
            elif len(cross_color) == 1:
                pm.draw_line(
                    start_point.x,
                    start_point.y,
                    end_point.x,
                    end_point.y,
                    color=pm_colors[cross_color[0]],
                    thick=1,
                )
            else:
                pm.draw_line(
                    start_point.x,
                    start_point.y,
                    end_point.x,
                    end_point.y,
                    color=pm_colors[cross_color[0]]
                    if p < 6
                    else pm_colors[cross_color[1]],
                    thick=1,
                )


class PlayerLabel:
    def __init__(
        self, position, text, size, scale_y, font_size, text_color, back_color
    ):
        text_length = pm.measure_text(text, font_size) - 4
        text_height = font_size + scale_y
        pad_height = (Cross.d * size - size / 2) * scale_y
        start_point_text = position - CSharpVector2(
            text_length / 2, text_height + pad_height
        )
        pm.draw_font(
            1,
            text,
            start_point_text.x + 4,
            start_point_text.y,
            font_size,
            0,
            pm_colors[text_color],
        )
        pm.draw_rectangle_rounded(
            start_point_text.x,
            start_point_text.y,
            text_length,
            font_size,
            0.8,
            1,
            pm_colors[back_color],
        )


class HostileLabel:
    def __init__(
        self, position, text, background_length, font_size, text_color, back_color
    ):
        pm.draw_font(
            1, text, position.x, position.y, font_size, 0, pm_colors[text_color]
        )
        pm.draw_rectangle_rounded(
            position.x,
            position.y,
            background_length,
            font_size,
            0.8,
            1,
            pm_colors[back_color],
        )


class TextBox:
    def __init__(
        self, position, text, width, height, font_size, text_color, back_color
    ):
        pm.draw_font(
            1, text, position.x, position.y, font_size, 0, pm_colors[text_color]
        )
        pm.draw_rectangle(position.x, position.y, width, height, pm_colors[back_color])
