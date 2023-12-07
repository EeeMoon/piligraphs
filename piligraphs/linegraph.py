from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .color import Color
from .size import Size
from .utils import get_color, limit, interpolate, Interpolation


class LineGraph(BaseGraph):
    """Class representing a Line graph."""
    def __init__(self,
                 *,
                 size: Size | tuple[int, int],
                 thickness: int = 1,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 point_width: int = 0,
                 all_points: bool = False,
                 num: int = -1,
                 kind: Interpolation = Interpolation.LINEAR) -> None:
        """
        LineGraph constructor.

        Attributes
        ----------
        size: `Size` | `tuple[int, int]`
            Graph image size.
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
        """
        super().__init__()

        self.size = size
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.point_width = point_width
        self.all_points = all_points
        self.num = num
        self.kind = kind

    @property
    def size(self) -> Size:
        """Graph size."""
        return self._size
    
    @size.setter
    def size(self, value: Size | tuple[int, int]):
        if not isinstance(value, Size): 
            value = Size(value)

        self._size = value

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

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', tuple(self.size))
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        draw = ImageDraw.Draw(image)
        thickness = self.thickness or 1
        num = self.num if self.num > 0 else num_items
        max_weight = max((i.weight for i in self.items))
        p_radius = self.point_width / 2 if self.point_width > 0 else thickness / 2
        limited_y = limit(
            [max_weight - item.weight for item in self.items], 
            p_radius, 
            self.size.height-p_radius)
        space_between_points = self.size.width / (num_items - 1)
        limited_x = limit(
            [space_between_points * i for i in range(num_items)], 
            p_radius, 
            self.size.width-p_radius)
        
        points = list(zip(limited_x, limited_y))
        smooth_points = interpolate(points, num, kind=self.kind)

        if self.fill:
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
                    (point[0] - p_radius, point[1] - p_radius,
                     point[0] + p_radius, point[1] + p_radius),
                     fill=self.outline.rgba, width=0)

        return image
