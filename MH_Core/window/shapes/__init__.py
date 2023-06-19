import math
import pyMeow as pm
from MH_Core.math import CSharpVector2


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





