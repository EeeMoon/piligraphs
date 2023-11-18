import numpy as np
from PIL import Image, ImageDraw

from .color import Color
from .utils import circle_xy


class RadarChartItem:
    """Class representing an item of radar chart."""
    def __init__(self,
                 *,
                 name: str | None = None,
                 value: int | float = 1) -> None:
        self.name: str | None = name
        self.value: int | float = value


class RadarChart:
    """Class representing a Radar chart."""
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int | None = None,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 width: int | None = None,
                 angle: int | None = None) -> None:
        self.radius: int = radius
        self.thickness: int | None = thickness

        self.fill: Color | None = None
        if fill is not None:
            self.fill = fill if isinstance(fill, Color) else Color(fill)

        self.outline: Color | None = None
        if outline is not None:
            self.outline = outline if isinstance(outline, Color) else Color(outline)

        self.width: int | None = width
        self.angle: int | None = angle
        self._items: list = []

    @property
    def radius(self) -> int:
        """Radar shape radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        self._radius = value    

    @property
    def thickness(self) -> int | None:
        """Stroke thickness."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int | None):
        self._thickness = value

    @property
    def fill(self) -> int | None:
        """Fill color."""
        return self._fill
    
    @fill.setter
    def fill(self, value: Color | None):
        self._fill = value

    @property
    def outline(self) -> int | None:
        """Outline color."""
        return self._outline
    
    @outline.setter
    def outline(self, value: Color | None):
        self._outline = value

    @property
    def width(self) -> int | None:
        """Stroke points width."""
        return self._width
    
    @width.setter
    def width(self, value: int | None):
        self._width = value

    @property
    def angle(self) -> int | None:
        """Chart start angle."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int | None):
        self._angle = value

    @property
    def items(self) -> list[RadarChartItem]:
        """Chart items."""
        return self._items
        

    def add_items(self, *items: RadarChartItem) -> None:
        """
        Add items to graph.

        Attributes
        ----------
        items: `RadarChartItem`
            Items to add.

        Raises
        ------
        `ValueError` if item is not of correct type.
        """
        for item in items:
            if not isinstance(item, RadarChartItem):
                raise ValueError(f"items must be instances of '{RadarChartItem.__name__}', not {type(item).__name__}")
            self._items.append(item)

    def remove_items(self, *items: RadarChartItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `RadarChartItem`
            Items to remove.

        Raises
        ------
        `ValueError` if item is not present.
        """
        for item in items:
            self._items.remove(item)

    def draw(self) -> Image.Image:
        """
        Draw a radar chart.
        """
        image = Image.new('RGB', (self.radius * 2,)*2)
        draw = ImageDraw.Draw(image)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        values = np.array([item.value for item in self.items])
        max_value = values.max()
        min_value = values.min()
        angle = 360 / num_items
        start_angle = self.angle or -90
        points = []

        lmax = self.radius - self.width - self.thickness
        lmin = self.radius / 100

        if max_value - min_value != 0:
            m = (lmax - lmin) / (max_value - min_value)
            b = lmax - m * max_value
            offsets = m * values + b
        else:
            offsets = [lmax for _ in values]

        for i, item in enumerate(self.items):
            points.append(circle_xy(self.radius, offsets[i], i * angle + start_angle))
        
        points.append(points[0])
        points.append(points[1])

        if self.fill is not None:
            draw.polygon(points, fill=self.fill.rgba, width=0)

        if self.outline is not None:
            draw.line(points,
                    fill=self.outline.rgba, 
                    width=self.thickness,
                    joint='curve')

            if self.width is not None:
                offset = abs(self.width) + self.thickness / 2

                for point in points:
                    draw.ellipse(((point[0] - offset, point[1] - offset), 
                                (point[0] + offset, point[1] + offset)),
                                fill=self.outline.rgba, width=0)

        return image
