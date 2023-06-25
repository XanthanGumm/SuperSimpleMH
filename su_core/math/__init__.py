import numpy as np
from typing import Self
np.set_printoptions(suppress=True)


class CSharpMatrix3X2:

    def __init__(self, zero_fill):
        if zero_fill:
            self._m = np.array(
                [[0., 0.],
                 [0., 0.],
                 [0., 0.]]
            )

        else:
            self._m = np.array(
                [[1., 0.],
                 [0., 1.],
                 [0., 0.]]
            )

    @classmethod
    def make_translation(cls, tx, ty):
        mat = cls(zero_fill=False)
        mat[2, 0] = tx
        mat[2, 1] = ty
        return mat

    @classmethod
    def make_rotation(cls, degrees: float | int):
        mat = cls(zero_fill=True)
        radians = np.deg2rad(degrees)
        if -1.74532943 * 10 ** -5 < radians < 1.74532943 * 10 ** -5:
            num1 = 1.0
            num2 = 0.0
        elif 1.57077887350062 < radians < 1.5708137800891731:
            num1 = 0.0
            num2 = 1.0
        elif -3.1415752002955166 > radians > 3.1415752002955166:
            num1 = -1.0
            num2 = 0.0
        elif -1.5708137800891731 < radians < -1.57077887350062:
            num1 = 0.0
            num2 = -1.0
        else:
            num1 = np.cos(radians)
            num2 = np.sin(radians)

        mat[0, 0] = num1
        mat[0, 1] = num2
        mat[1, 0] = 0. - num2
        mat[1, 1] = num1

        return mat

    @classmethod
    def make_scale(cls, sx: int | float, sy: int | float):
        mat = cls(zero_fill=True)
        mat[0, 0] = sx
        mat[1, 1] = sy

        return mat

    def __getitem__(self, item):
        return self._m[item]

    def __setitem__(self, key, value):
        self._m[key] = value

    def __matmul__(self, other: Self):
        if not isinstance(other, type(self)):
            raise TypeError("Not type of CSharpMatrix3X2 error.")

        m00 = self[0, 0] * other[0, 0] + self[0, 1] * other[1, 0]
        m01 = self[0, 0] * other[0, 1] + self[0, 1] * other[1, 1]
        m10 = self[1, 0] * other[0, 0] + self[1, 1] * other[1, 0]
        m11 = self[1, 0] * other[0, 1] + self[1, 1] * other[1, 1]
        m20 = self[2, 0] * other[0, 0] + self[2, 1] * other[1, 0] + other[2, 0]
        m21 = self[2, 0] * other[0, 1] + self[2, 1] * other[1, 1] + other[2, 1]

        self[0, 0] = m00
        self[0, 1] = m01
        self[1, 0] = m10
        self[1, 1] = m11
        self[2, 0] = m20
        self[2, 1] = m21

        return self

    def __rmatmul__(self, other):
        return self.__matmul__(other)

    def __repr__(self):
        return str(self._m)


class CSharpVector2:

    def __init__(self, x: float, y: float):
        self._x = None
        self._y = None
        self._angle = None
        self.update(x, y)

    def update(self, x, y):
        self._x = x
        self._y = y
        self._angle = np.arctan2(x, y)

    @classmethod
    def transform(cls, vec2: Self, mat: CSharpMatrix3X2):
        return cls(
            x=vec2.x * mat[0, 0] + vec2.y * mat[1, 0] + mat[2, 0],
            y=vec2.x * mat[0, 1] + vec2.y * mat[1, 1] + mat[2, 1]
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x):
        if not isinstance(x, float):
            raise TypeError("x is not a float number error.")
        self._x = x

    @y.setter
    def y(self, y):
        if not isinstance(y, float):
            raise TypeError("y is not a float number error.")
        self._y = y

    def multiply(self, sx, sy):
        x = self.x * sx
        y = self.y * sy
        return CSharpVector2(x, y)

    def add(self, ax, ay):
        x = self.x + ax
        y = self.y + ay
        return CSharpVector2(x, y)

    def rotate(self, angle):
        # angle = np.deg2rad(angle)
        x = self._x * np.cos(angle) - self._y * np.sin(angle)
        y = self._x * np.sin(angle) + self._y * np.cos(angle)
        return CSharpVector2(x, y)

    def __add__(self, other):
        return CSharpVector2(self._x + other.x, self._y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return CSharpVector2(self._x - other.x, self._y - other.y)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        return CSharpVector2(self._x * other, self._y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"(x={self.x}, y={self.y}, angle={np.rad2deg(self._angle)})"