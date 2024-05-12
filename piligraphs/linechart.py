from pinkie import Color
from typing import Literal
from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .utils import get_color, limit, interpolate


class LineChart(BaseGraph):
    """Class representing a Line Chart."""

    def __init__(
        self,
        size: tuple[int, int],
        *,
        thickness: int = 1,
        fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        pwidth: int = 0,
        onlysrc: bool = False,
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
        minh: int = 0
    ) -> None:
        """
        Attributes
        ----------
        size: `tuple[int, int]`
            Image width and height.
        thickness: `int`
            Line thickness.
        fill: `Color`
            Fill color. If = `...`, generates random color.
        outline: `Color`
            Line color. If = `...`, generates random color.
        pwidth: `int`
            Point width.
        onlysrc: `bool`
            To draw bold dots only in source points (without interpolated ones).
        npoints: `int`
            Number of points. If <= 0, equals to the number of items.
        interp: `Interpolation`
            Kind of interpolation. Used to make a smooth curve.
        minh: `int`
            Minimum height from the bottom of the graph.
        """
        super().__init__()

        self.size = size
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.pwidth = pwidth
        self.onlysrc = onlysrc
        self.npoints = npoints
        self.interp = interp
        self.minh = minh

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)

        w, h = self.size
        thickness = self.thickness or 1
        num = self.npoints if self.npoints > 0 else num_items
        max_weight = max((i.weight for i in self.items))
        pwidth = self.pwidth / 2 if self.pwidth > 0 else thickness / 2

        if max_weight == 0:
            lim_ys = [h - pwidth] * num_items
        else:
            lim_ys = limit(
                [max_weight - item.weight for item in self.items], 
                pwidth, 
                h - pwidth - self.minh
            )

        lim_xs = limit(
            [w / (num_items - 1) * i for i in range(num_items)], 
            pwidth, 
            w - pwidth
        )
        
        source_p = list(zip(lim_xs, lim_ys))
        smooth_p = interpolate(source_p, num, kind=self.interp)

        if self.fill:
            draw.polygon(
                [(pwidth, h)] + smooth_p + [(w - pwidth, h)],
                fill=self.fill.rgba, 
                width=0
            )

        if self.outline:
            draw.line(smooth_p, fill=self.outline.rgba, width=thickness, joint='curve')

            bald_p = (source_p[0], source_p[num_items-1])
            if self.pwidth:
                bald_p = source_p if self.onlysrc else smooth_p

            for p in bald_p:
                draw.ellipse(
                    (
                        p[0] - pwidth, p[1] - pwidth,
                        p[0] + pwidth, p[1] + pwidth
                    ),
                    fill=self.outline.rgba, 
                    width=0
                )

        return image
