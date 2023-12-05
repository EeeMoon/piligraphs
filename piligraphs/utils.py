import math
import enum
import numpy as np
from scipy.interpolate import interp1d


def rgb_to_hex(_rgb: tuple[int, int, int], /):
    return '{:02x}{:02x}{:02x}'.format(_rgb[0], _rgb[1], _rgb[2])


def hex_to_rgb(_hex: str, /):
    return tuple(int(_hex.strip('#')[i:i+2], 16) for i in (0, 2, 4))


def num_to_rgb(_num: int, /):
    return (
        (_num >> 16) & 255,
        (_num >> 8) & 255,
        _num & 255
    )


def rgb_to_num(_rgb: tuple[int, int, int], /):
    red, green, blue = _rgb
    return (red << 16) + (green << 8) + blue


def circle_xy(radius: int, distance: int, angle: int):
    angle_radians = math.radians(angle)
    x = radius + distance * math.cos(angle_radians)
    y = radius + distance * math.sin(angle_radians)
    return x, y


def get_color(color, /):
    """
    Returns
    -------
    `Color` or `None` if color is `None`.
    """
    from .color import Color

    if isinstance(color, Color):
        return color
    elif color is not None:
        return Color(color)
    else:
        return None
    

class Interpolation(enum.Enum):
    LINEAR = 'linear'
    NEAREST = 'nearest'
    NEAREST_UP = 'nearest-up'
    ZERO = 'zero'
    SLINEAR = 'slinear'
    QUADRATIC = 'quadratic'
    CUBIC = 'cubic'
    PREVIUOS = 'previous'
    NEXT = 'next'


def interpolate(
        points: list[tuple[int, int]], 
        num: int | None = None, 
        method: Interpolation = Interpolation.LINEAR) -> list[tuple[int, int]]:
    """
    Interpolate list of points to make a smooth curve.

    Attributes
    ----------
    points: `list[tuple[int, int]]`
        List of points. Every point must be a tuple containing 2 integers: x and y.
    num: `int` | `None`
        Number of points. If `None`, double the length of the list of points is set.
    method: `Interpolation`
        The kind of interpolation.
    """
    x, y = zip(*points)
    inter = interp1d(x, y, kind=method.value)

    if not num:
        num = len(points) * 2

    x_new = np.linspace(min(x), max(x), num)
    y_new = np.clip(inter(x_new), min(y), max(y))

    return list(zip(x_new, y_new))


def limit(
        values: list[int | float],
        minv: int | float,
        maxv: int | float,
        *,
        copy: bool = True) -> np.ndarray:
    """
    Limit array to specific range.

    Attributes
    ----------
    values: `list[int | float]`
        List of values.
    minv: `int | float`
        Minimum (bottom) value.
    maxv: `int | float`
        Maximum (top) value.
    copy: `bool`
        Copy an array or not.
    """
    array = np.array(values, copy=copy)
    _min, _max = min(array), max(array)

    if _max == _min:
        return array

    m = (maxv - minv) / (_max - _min)
    b = maxv - m * _max

    return m * array + b