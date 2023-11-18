import numpy as np
from PIL import Image, ImageDraw

from .color import Color
from .utils import circle_xy


class PieChartItem:
    """Class representing an item of pie chart."""
    def __init__(self,
                 *,
                 name: str, 
                 color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int],
                 value: int | float) -> None:
        self.name: str = name
        self.color: Color = color if isinstance(color, Color) else Color(color)
        self.value: int | float = value


class PieChart:
    """Class representing a pie chart."""
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int | None = None,
                 angle: int | None = None,
                 emboss: int | None = None,
                 border: int | None = None) -> None:
        """
        PieChart constructor.

        Attributes
        ----------
        radius: `int`
            Radius of the chart circle.
        thickness: `int` | `None`
            If None, graph will be pie-shaped.
            Otherwise, graph will be donut-shaped with specified thickness.
        angle: `int` | `None`
            Start angle of the chart.
        emboss `int` | `None`
            If None, graph will be flat. 
            Otherwise, graph parts will be different size based on value.
            If < 0, parts with higher value will be smaller.
        border: `int` | `None`
            Space between graph parts.
        """
        self.radius: int = radius
        self.thickness: int | None = thickness
        self.angle: int = angle
        self.emboss: int | None = emboss
        self.border = border
        self._items: list[PieChartItem] = []

    @property
    def radius(self) -> int:
        """Radius of the chart circle."""
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        if (hasattr(self, '_thickness') 
            and self.thickness is not None 
            and self.thickness > value):
            raise ValueError("attribute 'radius' can not be bigger than 'thickness'")
        self._radius = value    

    @property
    def thickness(self) -> int | None:
        """Thickness of the donut-shaped graph."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int | None):
        if (value is not None 
            and hasattr(self, '_radius') 
            and self.radius < value):
            raise ValueError("attribute 'thickness' can not be smaller than 'radius'")
        if (value is not None 
            and hasattr(self, '_emboss') 
            and self.emboss is not None 
            and abs(self.emboss) * 2 < value):
            raise ValueError("attribute 'thickness' can not be smaller than absolute value of 'emboss' twice")
        self._thickness = value

    @property
    def angle(self) -> int | None:
        """Start angle of the chart."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int | None):
        self._angle = value

    @property
    def emboss(self) -> int | None:
        """Max emboss of the graph parts."""
        return self._emboss
    
    @emboss.setter
    def emboss(self, value: int | None):
        if (value is not None 
            and hasattr(self, '_thickness') 
            and self.thickness is not None 
            and self.thickness < abs(value) * 2):
            raise ValueError("attribute 'emboss' can not be bigger than half of 'thickness'")
        self._emboss = value

    @property
    def border(self) -> int | None:
        """Space between chart parts."""
        return self._border
    
    @border.setter
    def border(self, value: int | None):
        self._border = value

    @property
    def items(self) -> list[PieChartItem]:
        """Chart items."""
        return self._items

    def add_items(self, *items: PieChartItem) -> None:
        """
        Add items to graph.

        Attributes
        ----------
        items: `CircleGraphItem`
            Items to add.

        Raises
        ------
        `ValueError` if item is not of correct type.
        """
        for item in items:
            if not isinstance(item, PieChartItem):
                raise ValueError(f"items must be instances of '{PieChartItem.__name__}', not {type(item).__name__}")
            self._items.append(item)

    def remove_items(self, *items: PieChartItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `CircleGraphItem`
            Items to remove.

        Raises
        ------
        `ValueError` if item is not present.
        """
        for item in items:
            self._items.remove(item)

    def draw(self) -> Image.Image:
        """
        Draw a circle graph.
        """
        image = Image.new('RGBA', (self.radius * 2,)*2)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        values = np.array([item.value for item in self.items])
        total_value = values.sum()
        max_value = values.max()
        min_value = values.min()
        start_angle = self.angle or 0
        thickness = self.thickness
        emboss = self.emboss or 0
        template = image.copy()

        m = (0 - emboss) / (max_value - min_value)
        b = emboss - m * min_value
        offsets = m * values + b

        if emboss < 0:
            offsets -= emboss

        for i, item in enumerate(self.items):
            img = template.copy()
            draw = ImageDraw.Draw(img)
            offset = offsets[i]

            if total_value == 0: 
                angle = 360 / num_items
            else:
                angle = 360 * item.value / total_value

            draw.pieslice(((0 + offset,)*2, (img.width - offset,)*2),
                          start_angle, start_angle + angle,
                          fill=item.color.rgba)
            
            if self.border:
                draw.line(((self.radius,)*2, circle_xy(self.radius, self.radius, start_angle + angle)),
                          fill=(0, 0, 0, 0), width=self.border)
                draw.line(((self.radius,)*2, circle_xy(self.radius, self.radius, start_angle)),
                          fill=(0, 0, 0, 0), width=self.border)
                draw.ellipse(((self.radius - self.border / 2,)*2, (self.radius + self.border / 2,)*2),
                             fill=(0, 0, 0, 0), width=0)
            
            if thickness:
                draw.ellipse(((thickness - offset,)*2, (self.radius * 2 - thickness + offset,)*2),
                             fill=(0, 0, 0, 0))
            
            image.alpha_composite(img)
            start_angle += angle

        return image


    