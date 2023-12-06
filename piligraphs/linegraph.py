import numpy as np
from PIL import Image, ImageDraw

from .item import GraphItem
from .color import Color
from .size import Size
from .utils import get_color, limit, interpolate, Interpolation


class LineGraph:
    """Class representing a Line graph."""
    def __init__(self,
                 *,
                 size: tuple[int, int],
                 thickness: int | None = None,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 point_width: int | None = None,
                 all_points: bool = False,
                 num: int | None = None,
                 kind: Interpolation = Interpolation.LINEAR) -> None:
        self.size = size
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.point_width = point_width
        self.all_points = all_points
        self.num = num
        self.kind = kind
        self._items: list[GraphItem] = []

    @property
    def size(self) -> Size:
        """Graph size."""
        return self._size
    
    @size.setter
    def size(self, value: tuple[int, int]):
        if not isinstance(value, Size): 
            value = Size(value)

        self._size = value

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
    def point_width(self) -> int | None:
        """Stroke points width."""
        return self._point_width
    
    @point_width.setter
    def point_width(self, value: int | None):
        self._point_width = value

    @property
    def all_points(self) -> bool:
        """Draw all points or not."""
        return self._all_points
    
    @all_points.setter
    def all_points(self, value: bool):
        self._all_points = value

    @property
    def num(self) -> int | None:
        """Number of points."""
        return self._num
    
    @num.setter
    def num(self, value: int | None):
        self._num = value

    @property
    def kind(self) -> Interpolation:
        """Kinf of interpolation."""
        return self._kind
    
    @kind.setter
    def kind(self, value: Interpolation):
        self._kind = value

    @property
    def items(self) -> list[GraphItem]:
        """Graph items."""
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
        Draw a Line graph.
        """
        image = Image.new('RGBA', tuple(self.size))
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)
        thickness = self.thickness or 1
        p_radius = self.point_width / 2 if self.point_width else thickness / 2
        limited_y = limit(
            [item.weight for item in self.items], 
            p_radius, 
            self.size.height-p_radius)
        space_between_points = self.size.width / (num_items - 1)
        limited_x = limit(
            [space_between_points * i for i in range(num_items)], 
            p_radius, 
            self.size.width-p_radius)
        
        points = list(zip(limited_x, limited_y))
        smooth_points = interpolate(points, self.num or num_items, kind=self.kind)

        if self.fill:
            # draw fill shape
            draw.polygon(
                [(p_radius, self.size.height)] 
                + smooth_points 
                + [(self.size.width-p_radius, self.size.height)],
                fill=self.fill.rgba, width=0)

        if self.outline:
            draw.line(smooth_points, fill=self.outline.rgba, width=thickness, joint='curve')

            big_points = (points[0], points[num_items-1])
            if self.point_width:
                big_points = smooth_points if self.all_points else points

            for point in big_points:
                draw.ellipse(
                    (point[0]-p_radius, point[1]-p_radius,
                     point[0]+p_radius, point[1]+p_radius),
                     fill=self.outline.rgba, width=0)

        return image
