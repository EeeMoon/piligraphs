from pinkie import Color
from typing import Literal
from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .utils import get_color, interpolate, linear_to_circle


class RadarChart(BaseGraph):
    """Class representing a Radar Chart."""

    def __init__(
        self,
        radius: int,
        *,
        thickness: int = 1,
        fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        pwidth: int = 0,
        onlysrc: bool = True,
        npoints: int = 0,
        interp: Literal[
            'linear',
            'nearest',
            'nearest-up',
            'zero',
            'slinear',
            'quadratic',
            'cubic',
            'previous',
            'next'
        ] = 'linear',
        angle: int = 0,
        minr: int = 0
    ) -> None:
        """
        Attributes
        ----------
        radius: `int`
            Radius of the chart shape.
        thickness: `int`
            Line thickness.
        fill: `Color`
            Fill color.
        outline: `Color`
            Line color.
        pwidth: `int`
            Point width.
        onlysrc: `bool`
            To draw bold dots only in source points (without interpolated ones).
        npoints: `int`
            Number of points. If <= 0, equals to the number of items.
        interp: `Interpolation`
            Kind of interpolation. Used to make a smooth curve.
        angle: `int`
            Start angle of the chart.
        minr: `int`
            Minimum distance between the center and a point.
        """
        super().__init__()

        self.radius = radius
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.pwidth = pwidth
        self.onlysrc = onlysrc
        self.npoints = npoints
        self.interp = interp
        self.angle = angle
        self.minr = minr

    def draw(self) -> Image.Image:
        w = self.radius * 2
        image = Image.new('RGBA', (w, w))

        if len(self.items) == 0:
            return image

        items = self.items.copy()
        items.append(items[0])
        num_items = len(items)
        
        draw = ImageDraw.Draw(image)

        thickness = self.thickness or 1
        num = self.npoints if self.npoints > 0 else num_items
        max_weight = max((i.weight for i in items))
        pwidth = self.pwidth / 2 if self.pwidth > 0 else thickness / 2
 
        source_p = list(zip(
            [w / (num_items - 1) * i for i in range(num_items)], 
            [max_weight - item.weight for item in items]
        ))
        smooth_p = interpolate(source_p, num, kind=self.interp)
        circle_p = linear_to_circle(
            smooth_p, 
            self.radius - self.pwidth, 
            self.minr,
            self.angle
        )

        if self.fill:
            draw.polygon(
                circle_p,
                fill=self.fill.rgba, 
                outline=self.outline.rgba,
                width=0
            )

        if self.outline:
            draw.line(
                circle_p, 
                fill=self.outline.rgba, 
                width=thickness, 
                joint='curve'
            )

            bold_p = (circle_p[0],)
            if self.pwidth > 0:
                step = num // num_items
                bold_p = circle_p[::step] if self.onlysrc and step else circle_p

            for p in bold_p:
                draw.ellipse(
                    (p[0] - pwidth, p[1] - pwidth,
                    p[0] + pwidth, p[1] + pwidth),
                    fill=self.outline.rgba, 
                    width=0
                )

        return image

