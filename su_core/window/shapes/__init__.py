import math
import pyMeow as pm
from su_core.math import CSharpVector2, CSharpMatrix3X2


class Arrow:
    orange = pm.get_color("orange")

    def __init__(self, start, end, short_render, text: str, color, start_pad):
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
            pm.draw_line(start.x, start.y, end.x, end.y, color=color, thick=2.0)

        pm.draw_text(text=text, posX=head_v3.x + 20, posY=head_v2.y - 5, fontSize=9, color=self.orange)
        pm.draw_triangle(head_v1.x, head_v1.y, head_v2.x, head_v2.y, head_v3.x, head_v3.y, color=color)


class Cross:
    colors = {"saddlebrown": pm.get_color("saddlebrown"), "gold": pm.get_color("gold"), "red": pm.get_color("red"),
              "yellow": pm.get_color("yellow"), "blue": pm.get_color("blue"), "green": pm.get_color("green"),
              "white": pm.get_color("white"), "salmon": pm.get_color("salmon"), "cyan": pm.get_color("cyan",),
              "royalblue": pm.get_color("royalblue"), "seagreen": pm.get_color("seagreen")}
    a, b, c, d = 0.25, 0.5, 0.75, 1.0
    points = CSharpVector2(0, a), CSharpVector2(a, 0), CSharpVector2(b, a), CSharpVector2(c, 0), \
             CSharpVector2(d, a), CSharpVector2(c, b), CSharpVector2(d, c), CSharpVector2(c, d), \
             CSharpVector2(b, c), CSharpVector2(a, d), CSharpVector2(0, c), CSharpVector2(a, b), \
             CSharpVector2(0, a)

    def __init__(self, position, size, scale_x, scale_y, colors):
        for p in range(1, 13):
            start_point = position + (self.points[p - 1].multiply(size, size) - CSharpVector2(size / 2, size / 2)).multiply(scale_x, scale_y)
            end_point = position + (self.points[p].multiply(size, size) - CSharpVector2(size / 2, size / 2)).multiply(scale_x, scale_y)

            if len(colors) == 0:
                pm.draw_line(start_point.x, start_point.y, end_point.x, end_point.y,
                             color=self.colors["white"], thick=1)
            elif len(colors) == 1:
                pm.draw_line(start_point.x, start_point.y, end_point.x, end_point.y,
                             color=self.colors[colors[0]], thick=1)
            else:
                pm.draw_line(start_point.x, start_point.y, end_point.x, end_point.y,
                             color=self.colors[colors[0]] if p < 6 else self.colors[colors[1]], thick=1)
