import numpy as np
from pinkie import Color
from typing import Callable
from PIL import Image, ImageDraw

from .graph import Graph
from .utils import get_color


class FuncGraph(Graph):
    """
    Class representing a function graph.

    ## WARNING
    `tan()` and similar functions can be drawn incorrectly
    since we cannot determine the asymptotes automatically.
    Instead of using raw `tan()`, you should make a custom solution:
    ```
    res_x, res_y = (40, 40)

    def tangent(x: float) -> float | None:
        step = math.pi
        diap = 1 / (res_x * 3)
        current = math.pi / 2
        while current < res_x:
            if abs(x) > current - diap and abs(x) < current + diap:
                return None
            current += step
        return math.tan(x)

    graph = FuncGraph(
        (1000, 1000), 
        func=tangent, 
        thickness=16,
        res=(res_x, res_y),
        step=0.1
    )
    ```
    """

    def __init__(
        self,
        size: tuple[int, int],
        *,
        func: Callable[[float], float],
        thickness: int = 1,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        res: tuple[int, int] = (10, 10),
        step: int | float = 1
    ) -> None:
        """
        Attributes
        ----------
        size: `tuple[int, int]`
            Image width and height.
        func: `Callable[[float], float]`
            Function for building a graph based on.
        thickness: `int`
            Line thickness.
        outline: `Color`
            Line color. If = `...`, generates a random color.
        res: `tuple[int, int]`
            Numbers of points from the center to x and y end respectively.
        step: `int` | `float`
            Quality of the graph. Lower value = smoother result.
        """
        super().__init__()

        self.size = size
        self.func = func
        self.thickness = thickness
        self.outline = get_color(outline)
        self.res = res
        self.step = step
    
    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(image)

        w, h = self.size
        func = self.func
        thickness = self.thickness
        radius = thickness // 2
        res_x, res_y = self.res
        outline_rgba = self.outline.rgba
        lines: list[list[tuple[float, float]]] = [[]]
        
        for x in np.arange(radius, w - radius, self.step):
            try:
                x_val = (x / w - 0.5) * 2 * res_x
                y_val = func(x_val)

                if y_val is None:
                    lines.append([])
                    continue

                y = h - (y_val / (2 * res_y) + 0.5) * h
                    
                lines[-1].append((x, y))
            except Exception:
                lines.append([])
        
        for line in lines:
            if len(line) == 0:
                continue
            
            draw.line(line, fill=outline_rgba, width=thickness, joint='curve')

            for x, y in (line[0], line[-1]):
                draw.ellipse(
                    (
                        (x - radius, y - radius),
                        (x + radius, y + radius)
                    ),
                    fill=outline_rgba,
                    width=0
                )
        
        return image


