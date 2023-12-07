import math
import enum
import random
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
    elif color == ...:
        return Color((
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))
    elif color is not None:
        return Color(color)
    else:
        return Color((0, 0, 0, 0))
    

class Interpolation(enum.Enum):
    """
    Interpolation type.
    """
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
        kind: Interpolation = Interpolation.LINEAR) -> list[tuple[int, int]]:
    """
    Interpolate list of points to make a smooth curve.

    Attributes
    ----------
    points: `list[tuple[int, int]]`
        List of points. Every point must be a tuple containing 2 integers: x and y.
    num: `int` | `None`
        Number of points. If `None`, double the length of the list of points is set.
    kind: `Interpolation`
        The kind of interpolation.
    """
    x, y = zip(*points)
    inter = interp1d(x, y, kind=kind.value)

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


def interpolate_circle(
        points: list[tuple[int, int]], 
        num: int | None = None, 
        kind: Interpolation = Interpolation.LINEAR) -> list[tuple[int, int]]:
    """
    Interpolate list of points distributed around a circle to make a smooth curve.

    Attributes
    ----------
    points: `List[Tuple[int, int]]`
        List of points. Every point must be a tuple containing 2 integers: angle and radius.
    num: `int` | `None`
        Number of points. If `None`, double the length of the list of points is set.
    kind: `Interpolation`
        The kind of interpolation.
    """
    angles, radii = zip(*points)
    angles = np.deg2rad(angles)  # Convert angles to radians

    inter = interp1d(angles, radii, kind=kind.value)

    if not num:
        num = len(points) * 2

    angles_new = np.linspace(min(angles), max(angles), num)
    radii_new = np.clip(inter(angles_new), min(radii), max(radii))

    x_new = radii_new * np.cos(angles_new)
    y_new = radii_new * np.sin(angles_new)

    return list(zip(x_new, y_new))


def linear_to_circle(
        points: list[tuple[int, int]], 
        radius: int, 
        min_radius: int = 0, 
        angle: int = 360) -> list[tuple[int, int]]:
    """
    Convert linear points to circular.

    Attributes
    ----------
    points: `list[tuple[int, int]]`
        List of points.
    radius: `int`
        Max radius.
    min_radius: `int`
        Min radius.
    angle: `int`
        Angle.
    """
    y = [p[1] for p in points]
    max_y = max(y)
    ang = angle / (len(points) - 1)
    radii = limit([max_y - i for i in y], min_radius, radius)

    return [
        circle_xy(radius, rad, i * ang)
        for i, rad in enumerate(radii)
    ]