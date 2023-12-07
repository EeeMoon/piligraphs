import numpy as np
from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .color import Color
from .utils import circle_xy, get_color, limit, interpolate, Interpolation, linear_to_circle


class RadarChart(BaseGraph):
    """Class representing a Radar chart."""
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int = 1,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 point_width: int = 0,
                 all_points: bool = False,
                 num: int = -1,
                 kind: Interpolation = Interpolation.LINEAR,
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
        all_points: `bool`
            If `True`, all points (including intermediate ones) will be drawn.
            Otherwise, only source points will be displayed.
        num: `int`
            Number of points. If < 0, equals to the number of items.
        kind: `Interpolation`
            Kind of interpolation. Used to make a smooth curve.
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
        self.all_points = all_points
        self.num = num
        self.kind = kind
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
    def all_points(self) -> bool:
        """Draw all points or not."""
        return self._all_points
    
    @all_points.setter
    def all_points(self, value: bool):
        self._all_points = value

    @property
    def num(self) -> int:
        """Number of points."""
        return self._num
    
    @num.setter
    def num(self, value: int):
        self._num = value

    @property
    def kind(self) -> Interpolation:
        """Kinf of interpolation."""
        return self._kind
    
    @kind.setter
    def kind(self, value: Interpolation):
        self._kind = value

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
        items = self.items
        items.append(items[0])
        num_items = len(items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)
        thickness = self.thickness or 1
        num = self.num if self.num > 0 else num_items
        max_weight = max((i.weight for i in items))
        p_radius = self.point_width / 2 if self.point_width > 0 else thickness / 2
        space_between_points = image.size[0] / (num_items - 1)
      
        points = list(zip([space_between_points * i for i in range(num_items)], 
                          [max_weight - item.weight for item in items]))
        smooth_points = interpolate(points, num, kind=self.kind)
        c_points = linear_to_circle(points, self.radius - self.point_width, self.min_radius)
        c_smooth_points = linear_to_circle(smooth_points, self.radius - self.point_width, self.min_radius)

        if self.fill:
            draw.polygon(
                c_smooth_points,
                fill=self.fill.rgba, 
                outline=self.outline.rgba,
                width=0)

        if self.outline:
            draw.line(c_smooth_points + [c_smooth_points[0]], 
                      fill=self.outline.rgba, 
                      width=thickness, 
                      joint='curve')

            big_points = (c_smooth_points[0],)
            if self.point_width > 0:
                big_points = c_smooth_points if self.all_points else c_points

            for point in big_points:
                draw.ellipse(
                    (point[0] - p_radius, point[1] - p_radius,
                    point[0] + p_radius, point[1] + p_radius),
                    fill=self.outline.rgba, width=0)

        return image

