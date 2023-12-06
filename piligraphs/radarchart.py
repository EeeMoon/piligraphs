import numpy as np
from PIL import Image, ImageDraw

from .item import GraphItem
from .color import Color
from .utils import circle_xy, get_color, limit


class RadarChart:
    """Class representing a Radar chart."""
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int | None = None,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 point_width: int | None = None,
                 angle: int | None = None,
                 min_radius: int | None = None) -> None:
        self.radius = radius
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.point_width = point_width
        self.angle = angle
        self.min_radius = min_radius
        self._items: list[GraphItem] = []

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
    def thickness(self) -> int | None:
        """Stroke thickness."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int | None):
        self._thickness = value

    @property
    def fill(self) -> Color | None:
        """Fill color."""
        return self._fill
    
    @fill.setter
    def fill(self, value: Color | None):
        self._fill = value

    @property
    def outline(self) -> Color | None:
        """Outline color."""
        return self._outline
    
    @outline.setter
    def outline(self, value: Color | None):
        self._outline = value

    @property
    def point_width(self) -> int | None:
        """Stroke points width."""
        return self._point_width
    
    @point_width.setter
    def point_width(self, value: int | None):
        self._point_width = value

    @property
    def angle(self) -> int | None:
        """Chart start angle."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int | None):
        self._angle = value

    @property
    def min_radius(self) -> int | None:
        """Minimum distance between center and point."""
        return self._min_radius
    
    @min_radius.setter
    def min_radius(self, value: int | None):
        if (hasattr(self, '_radius')
            and value is not None
            and self.radius < value):
            raise ValueError("'min_radius' can not be bigger than 'radius'")
        self._min_radius = value

    @property
    def items(self) -> list[GraphItem]:
        """Chart items."""
        return self._items.copy()
        
    def add_items(self, *items: GraphItem) -> None:
        """
        Add items to graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to add.

        Raises
        ------
        `ValueError` if item is not of correct type.
        """
        for item in items:
            if not isinstance(item, GraphItem):
                raise ValueError(f"items must be instances of '{GraphItem.__name__}', not {type(item).__name__}")
            self._items.append(item)

    def remove_items(self, *items: GraphItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to remove.

        Raises
        ------
        `ValueError` if item is not present.
        """
        for item in items:
            self._items.remove(item)

    def draw(self) -> Image.Image:
        """
        Draw a Radar chart.
        """
        image = Image.new('RGB', (self.radius * 2,)*2)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)
        thickness = self.thickness or self.radius / 5
        weights = np.array([item.weight for item in self.items])
        angle = 360 / num_items
        start_angle = self.angle or -90
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
