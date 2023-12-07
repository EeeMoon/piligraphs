from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .utils import circle_xy, limit


class PieChart(BaseGraph):
    """Class representing a Pie chart."""
    def __init__(self,
                 *,
                 radius: int,
                 width: int = 0,
                 angle: int = 0,
                 emboss: int = 0,
                 space_between: int = 0) -> None:
        """
        PieChart constructor.

        Attributes
        ----------
        radius: `int`
            Radius of the chart circle.
        width: `int`
            If None, graph will be pie-shaped.
            Otherwise, graph will be donut-shaped with specified thickness.
        angle: `int`
            Start angle of the chart.
        emboss: `int`
            If = 0, graph will be flat. 
            Otherwise, graph parts will be different size based on value.
            If < 0, parts with higher weight will be smaller.
        space_between: `int`
            Space between graph parts.
        """
        super().__init__()

        self.radius = radius
        self.width = width
        self.angle = angle
        self.emboss = emboss
        self.space_between = space_between

    @property
    def radius(self) -> int:
        """Chart circle radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        if (hasattr(self, '_thickness')
            and self.width > value):
            raise ValueError("'radius' can not be smaller than 'thickness'")
        self._radius = value

    @property
    def width(self) -> int:
        """Width of the donut-shaped graph."""
        return self._width
    
    @width.setter
    def width(self, value: int):
        if (hasattr(self, '_radius') 
            and self.radius < value):
            raise ValueError("'thickness' can not be bigger than 'radius'")
        if (hasattr(self, '_emboss') 
            and abs(self.emboss) * 2 < value):
            raise ValueError("'thickness' can not be bigger than absolute value of 'emboss' twice")
        self._width = value

    @property
    def angle(self) -> int:
        """Chart start angle"""
        return self._angle
    
    @angle.setter
    def angle(self, value: int):
        self._angle = value

    @property
    def emboss(self) -> int:
        """Graph parts max emboss."""
        return self._emboss
    
    @emboss.setter
    def emboss(self, value: int):
        if (hasattr(self, '_thickness') 
            and self.width < abs(value) * 2):
            raise ValueError("'emboss' can not be bigger than half of 'thickness'")
        self._emboss = value

    @property
    def space_between(self) -> int:
        """Space between chart parts."""
        return self._space_between
    
    @space_between.setter
    def space_between(self, value: int):
        self._space_between = value

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', (self.radius * 2,)*2)
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        weights = [item.weight for item in self.items]
        total_weight = sum(weights)
        start_angle = self.angle
        width = self.width
        emboss = self.emboss
        template = image.copy()

        offsets = limit(
            weights, 
            0 if emboss < 0 else abs(emboss), 
            abs(emboss) if emboss < 0 else 0)

        for i, item in enumerate(self.items):
            img = template.copy()
            draw = ImageDraw.Draw(img)
            offset = offsets[i]

            if total_weight == 0: 
                angle = 360 / num_items
            else:
                angle = 360 * item.weight / total_weight

            if item.color is not None:
                draw.pieslice(((0 + offset,)*2, (img.width - offset,)*2),
                            start_angle, start_angle + angle,
                            fill=item.color.rgba)
                
                if self.space_between > 0:
                    draw.line(((self.radius,)*2, circle_xy(self.radius, self.radius, start_angle + angle)),
                            fill=(0, 0, 0, 0), width=self.space_between)
                    draw.line(((self.radius,)*2, circle_xy(self.radius, self.radius, start_angle)),
                            fill=(0, 0, 0, 0), width=self.space_between)
                    draw.ellipse(((self.radius - self.space_between / 2,)*2, (self.radius + self.space_between / 2,)*2),
                                fill=(0, 0, 0, 0), width=0)
            
                if width > 0:
                    draw.ellipse(((width - offset,)*2, (self.radius * 2 - width + offset,)*2),
                                fill=(0, 0, 0, 0))
            
                image.alpha_composite(img)

            start_angle += angle

        return image


    