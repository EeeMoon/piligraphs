from .color import Color
from .utils import get_color


class GraphItem:
    """Class representing a graph item."""
    def __init__(self,
                 *,
                 color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 weight: int | float = 1) -> None:
        self.color = get_color(color)
        self.weight = weight

    @property
    def color(self) -> Color | None:
        return self._color
    
    @color.setter
    def color(self, value: Color):
        self._color = get_color(value)

    @property
    def weight(self) -> int | float:
        return self._weight
    
    @weight.setter
    def weight(self, value: int | float):
        self._weight = value
    