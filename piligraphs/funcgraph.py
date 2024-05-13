import numpy as np
from pinkie import Color
from typing import Callable
from PIL import Image, ImageDraw

from .chart import Chart
from .utils import get_color


class FuncGraph(Chart):
    """Class representing a function graph."""

    def __init__(
        self,
        size: tuple[int, int],
        *,
        func: Callable[[int | float], int | float],
        thickness: int = 1,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        resolution: int = 10,
    ) -> None:
        super().__init__()

        self.size = size
        self.func = func
        self.thickness = thickness
        self.outline = get_color(outline)
        self.resolution = resolution

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(image)

        w, h = self.size
        func = self.func
        thickness = self.thickness
        radius = thickness // 2
        res = self.resolution

        xs = np.arange(radius, w - radius, radius)
        x_values = (xs / w - 0.5) * 2 * res
        y_values = np.array([func(i) for i in x_values])
        ys = h - (y_values / (2 * res) + 0.5) * h
        points = list(zip(xs, ys))

        draw.line(points, fill=self.outline.rgba, width=thickness, joint='curve')
        
        for x, y in (points[0], points[-1]):
            draw.ellipse(
                (
                    (x - radius, y - radius),
                    (x + radius, y + radius)
                ),
                fill=self.outline.rgba,
                width=0
            )
        
        return image
