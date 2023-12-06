import numpy as np
from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .color import Color
from .utils import circle_xy, get_color, limit


class RadarChart(BaseGraph):
    """Class representing a Radar chart."""
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int = 1,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 point_width: int = 0,
                 angle: int = 270,
                 min_radius: int = 0) -> None:
        """
        RadarChart constructor.

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
        point_width: `int`
            Point width.
        angle: `int`
            Start angle of the chart.
        min_radius: `int`
            Minimum distance between the center and the point.
        """
        super().__init__()

        self.radius = radius
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.point_width = point_width
        self.angle = angle
        self.min_radius = min_radius

    @property
    def radius(self) -> int:
        """Radar shape radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        if (hasattr(self, '_min_radius') 
            and self.min_radius > value):
            raise ValueError("'radius' can not be smaller than 'minimum'")
        self._radius = value

    @property
    def thickness(self) -> int:
        """Stroke thickness."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int):
        self._thickness = value

    @property
    def fill(self) -> Color:
        """Fill color."""
        return self._fill
    
    @fill.setter
    def fill(self, value: Color):
        self._fill = value

    @property
    def outline(self) -> Color:
        """Outline color."""
        return self._outline
    
    @outline.setter
    def outline(self, value: Color):
        self._outline = value

    @property
    def point_width(self) -> int:
        """Stroke points width."""
        return self._point_width
    
    @point_width.setter
    def point_width(self, value: int):
        self._point_width = value

    @property
    def angle(self) -> int | None:
        """Chart start angle."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int):
        self._angle = value

    @property
    def min_radius(self) -> int:
        """Minimum distance between center and point."""
        return self._min_radius
    
    @min_radius.setter
    def min_radius(self, value: int):
        if (hasattr(self, '_radius')
            and self.radius < value):
            raise ValueError("'min_radius' can not be bigger than 'radius'")
        self._min_radius = value

    def draw(self) -> Image.Image:
        image = Image.new('RGB', (self.radius * 2,)*2)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)
        thickness = self.thickness
        weights = np.array([item.weight for item in self.items])
        angle = 360 / num_items
        start_angle = self.angle
        points = []

        offsets = limit(
            weights,
            self.min_radius,
            self.radius - self.point_width - self.thickness)
                        
        for i in range(num_items):
            points.append(circle_xy(self.radius, offsets[i], i * angle + start_angle))
        
        points.append(points[0])
        points.append(points[1])

        if self.fill:
            draw.polygon(points, fill=self.fill.rgba, width=0)

        if self.outline:
            draw.line(points,
                    fill=self.outline.rgba, 
                    width=thickness,
                    joint='curve')

            if self.point_width:
                offset = self.point_width + thickness / 2

                for point in points:
                    draw.ellipse(((point[0] - offset, point[1] - offset), 
                                (point[0] + offset, point[1] + offset)),
                                fill=self.outline.rgba, width=0)

        return image
