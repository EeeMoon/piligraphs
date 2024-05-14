from pinkie import Color
from typing import Literal
from PIL import Image, ImageDraw

from .graph import NodeGraph
from .utils import get_color, interpolate, linear_to_circle


class RadarChart(NodeGraph):
    """Class representing a radar chart."""

    def __init__(
        self,
        radius: int,
        *,
        thickness: int = 1,
        fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        pwidth: int = 0,
        onlysrc: bool = True,
        npoints: int | None = None,
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
            Fill color. If = `...`, generates a random color.
        outline: `Color`
            Line color. If = `...`, generates a random color.
        pwidth: `int`
            Point width.
        onlysrc: `bool`
            To draw bold dots only in source points (without interpolated ones).
        npoints: `int` | `None`
            Number of points. If `None`, equals to the number of nodes.
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

        if len(self.nodes) == 0:
            return image

        nodes = self.nodes.copy()
        nodes.append(nodes[0])
        num_nodes = len(nodes)
        
        draw = ImageDraw.Draw(image)

        thickness = self.thickness
        num = self.npoints if self.npoints is not None else num_nodes
        max_weight = max((i.weight for i in nodes))
        radius = self.pwidth / 2 if self.pwidth > 0 else thickness / 2
 
        source_p = list(zip(
            [w / (num_nodes - 1) * i for i in range(num_nodes)], 
            [max_weight - node.weight for node in nodes]
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
                step = num // num_nodes
                bold_p = circle_p[::step] if self.onlysrc and step else circle_p

            for p in bold_p:
                draw.ellipse(
                    (p[0] - radius, p[1] - radius,
                    p[0] + radius, p[1] + radius),
                    fill=self.outline.rgba, 
                    width=0
                )

        return image

