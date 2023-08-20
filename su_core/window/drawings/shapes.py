import math
import pyMeow as pm
from su_core.math import CSharpVector2
from su_core.window.drawings import pm_colors


# TODO: continue refactor this file
def draw_arrow_shape(start, end, padding, gamma, color, text="", font_size=0, text_color="orange"):
    head_v1 = CSharpVector2(-0.6, 0.0) * gamma  # left vertex
    head_v2 = CSharpVector2(0.0, math.sqrt(3) / 2) * gamma  # middle vertex
    head_v3 = CSharpVector2(0.6, 0.0) * gamma  # right vertex

    x_len = end.x - start.x
    y_len = end.y - start.y

    rot_angle = math.atan2(x_len, y_len)

    # add padding from the starting point
    start = start.rotate(rot_angle)
    start.y += padding
    start = start.rotate(-rot_angle)

    # add padding from the ending point
    end = end.rotate(rot_angle)
    end.y -= gamma // 3
    end = end.rotate(-rot_angle)

    head_v1 = head_v1.rotate(-rot_angle) + end
    head_v2 = head_v2.rotate(-rot_angle) + end
    head_v3 = head_v3.rotate(-rot_angle) + end

    # add padding from the head
    end = end.rotate(rot_angle)
    end.y -= gamma // 5
    end = end.rotate(-rot_angle)

    if text:
        pm.draw_text(
            text=text,
            posX=head_v3.x + 20,
            posY=head_v2.y - 5,
            fontSize=font_size,
            color=pm_colors[text_color],
        )

    pm.draw_line(
        start.x,
        start.y,
        end.x,
        end.y,
        color=pm_colors[color],
        thick=2.0,
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
                self.points[p - 1].multiply(size, size) - CSharpVector2(size / 2, size / 2)
            ).multiply(scale_x, scale_y)
            end_point = position + (self.points[p].multiply(size, size) - CSharpVector2(size / 2, size / 2)).multiply(
                scale_x, scale_y
            )

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
                    color=pm_colors[cross_color[0]] if p < 6 else pm_colors[cross_color[1]],
                    thick=1,
                )


def draw_label_shape(
    text: str,
    position: CSharpVector2,
    text_width: int,
    font_size: int,
    text_color: str,
    background_color: str,
):
    pm.draw_font(
        1,
        text,
        position.x,
        position.y,
        font_size,
        0,
        pm_colors[text_color],
    )

    pm.draw_rectangle_rounded(
        position.x - font_size // 2,
        position.y,
        text_width + font_size,
        font_size,
        0.8,
        0,
        pm_colors[background_color],
    )
