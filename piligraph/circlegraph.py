import numpy as np
from PIL import Image, ImageDraw

from .graphitem import GraphItem


class CircleGraph:
    def __init__(self,
                 *,
                 radius: int,
                 thickness: int | None = None,
                 angle: int | None = None,
                 emboss: int | None = None) -> None:
        self.radius: int = radius
        self.thickness: int | None = thickness
        self.angle: int = angle
        self.emboss: int | None = emboss
        self._items: list[GraphItem] = []

    @property
    def radius(self) -> int:
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        if hasattr(self, '_thickness') and self.thickness is not None and self.thickness > value:
            raise ValueError("attribute 'radius' can not be bigger than 'thickness'")
        self._radius = value    

    @property
    def thickness(self) -> int | None:
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int | None):
        if hasattr(self, '_radius') and self.radius < value:
            raise ValueError("attribute 'thickness' can not be smaller than 'radius'")
        if hasattr(self, '_emboss') and self.emboss is not None and abs(self.emboss) * 2 < value:
            raise ValueError("attribute 'thickness' can not be smaller than absolute value of 'emboss' twice")
        self._thickness = value

    @property
    def angle(self) -> int | None:
        return self._angle
    
    @angle.setter
    def angle(self, value: int | None):
        self._angle = value

    @property
    def emboss(self) -> int | None:
        return self._emboss
    
    @emboss.setter
    def emboss(self, value: int | None):
        if hasattr(self, '_thickness') and self.thickness is not None and self.thickness < abs(value) * 2:
            raise ValueError("attribute 'emboss' can not be bigger than half of 'thickness'")
        self._emboss = value

    @property
    def items(self) -> list[GraphItem]:
        return self._items

    def add_items(self, *items: GraphItem) -> None:
        for item in items:
            self._items.append(item)

    def remove_items(self, *items: GraphItem) -> None:
        for item in items:
            self._items.remove(item)

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', (self.radius*2,)*2)
        num_items = len(self.items)
    
        if num_items == 0: 
            return image
        
        values = np.array([item.value for item in self.items])
        total_value = values.sum()
        max_value = values.max()
        min_value = values.min()
        start_angle = self.angle or 0
        template = image.copy()
        thickness = self.thickness
        emboss = self.emboss or 0

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
                          fill=item.color.rgb)
            
            if thickness:
                draw.ellipse(((thickness - offset,)*2, (self.radius * 2 - thickness + offset,)*2), 
                             fill=(0, 0, 0, 0))
            
            image.alpha_composite(img)
            start_angle += angle

        return image


    