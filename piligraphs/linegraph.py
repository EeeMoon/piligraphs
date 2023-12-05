import numpy as np
from PIL import Image, ImageDraw

from .color import Color
from .size import Size
from .utils import get_color


class LineGraphItem:
    """Class representing an item of line graph."""
    def __init__(self,
                 *,
                 name: str | None = None,
                 weight: int | float = 1) -> None:
        self.name: str | None = name
        self.weight: int | float = weight


class LineGraph:
    """Class representing a Line graph."""
    def __init__(self,
                 *,
                 size: tuple[int, int],
                 thickness: int | None = None,
                 fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 point_width: int | None = None) -> None:
        self.size = size
        self.thickness = thickness
        self.fill = get_color(fill)
        self.outline = get_color(outline)
        self.point_width = point_width
        self._items: list[LineGraphItem] = []

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
    def items(self) -> list[LineGraphItem]:
        """Graph items."""
        return self._items.copy()
        
    def add_items(self, *items: LineGraphItem) -> None:
        """
        Add items to graph.

        Attributes
        ----------
        items: `LineGraphItem`
            Items to add.

        Raises
        ------
        `ValueError` if item is not of correct type.
        """
        for item in items:
            if not isinstance(item, LineGraphItem):
                raise ValueError(f"items must be instances of '{LineGraphItem.__name__}', not {type(item).__name__}")
            self._items.append(item)

    def remove_items(self, *items: LineGraphItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `LineGraphItem`
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
        pass
