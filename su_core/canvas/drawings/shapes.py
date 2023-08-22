import math
import pyMeow as pm
from su_core.math import CSharpVector2
from su_core.canvas.drawings import pm_colors


def draw_arrow_shape(
    start,
    end,
    padding,
    gamma,
    color,
    text="",
    font_size=0,
    text_color="Orange",
):
    """

    :param start: source position
    :param end: destination position
    :param padding: padding from start position regardless the direction.
    :param gamma: scalar which controls the head of the arrow
    :param color: color of the arrow
    :param text: (optional) text to display at the head of the arrow
    :param font_size: (optional) font size of the text
    :param text_color: (optional) color of the text
    :return:
    """
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


def draw_label_shape(
    text: str,
    position: CSharpVector2,
    text_width: int,
    font_size: int,
    text_color: str,
    background_color: str,
):
    pm.draw_rectangle_rounded(
        position.x - font_size // 2,
        position.y,
        text_width + font_size,
        font_size,
        0.8,
        0,
        pm_colors[background_color],
    )

    pm.draw_font(
        1,
        text,
        position.x,
        position.y,
        font_size,
        0,
        pm_colors[text_color],
    )

    # pm.draw_rectangle_rounded(
    #     position.x - font_size // 2,
    #     position.y,
    #     text_width + font_size,
    #     font_size,
    #     0.8,
    #     0,
    #     pm_colors[background_color],
    # )


def draw_cross_shape(position, beta, gamma, color, color2="", multiplayer=6, thickness=1):
    """
    :param position: center of the cross
    :param beta: width scalar
    :param gamma: height scalar
    :param color: color of the cross
    :param color2: second color if passed the crossed will be colored in two colors
    :param multiplayer: the multiplayer of beta and gamma (do not touch)
    :param thickness: thickness of the cross
    """
    for i in range(1, 13):
        start = draw_cross_shape.points[i - 1].multiply(multiplayer, multiplayer) - multiplayer / 2
        start = start.multiply(beta, gamma) + position
        end = draw_cross_shape.points[i].multiply(multiplayer, multiplayer) - multiplayer / 2
        end = end.multiply(beta, gamma) + position
        pm.draw_line(
            start.x,
            start.y,
            end.x,
            end.y,
            color=pm_colors[color] if 2 < i < 9 or not color2 else pm_colors[color2],
            thick=thickness,
        )


draw_cross_shape.a = 0.25
draw_cross_shape.b = 0.5
draw_cross_shape.c = 0.75
draw_cross_shape.d = 1.0
draw_cross_shape.points = (
    CSharpVector2(0, draw_cross_shape.a),
    CSharpVector2(draw_cross_shape.a, 0),
    CSharpVector2(draw_cross_shape.b, draw_cross_shape.a),
    CSharpVector2(draw_cross_shape.c, 0),
    CSharpVector2(draw_cross_shape.d, draw_cross_shape.a),
    CSharpVector2(draw_cross_shape.c, draw_cross_shape.b),
    CSharpVector2(draw_cross_shape.d, draw_cross_shape.c),
    CSharpVector2(draw_cross_shape.c, draw_cross_shape.d),
    CSharpVector2(draw_cross_shape.b, draw_cross_shape.c),
    CSharpVector2(draw_cross_shape.a, draw_cross_shape.d),
    CSharpVector2(0, draw_cross_shape.c),
    CSharpVector2(draw_cross_shape.a, draw_cross_shape.b),
    CSharpVector2(0, draw_cross_shape.a),
)