from pinkie import Color


class Node:
    """Class representing a graph node."""

    def __init__(
        self,
        *,
        weight: int | float = 1,
        color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...
    ) -> None:
        self.weight = weight
        self.color = color

    @property
    def weight(self) -> int:
        """Node weight."""
        return self._weight
    
    @weight.setter
    def weight(self, value: int | float):
        self._weight = value
  
    @property
    def color(self) -> Color | None:
        """Node color."""
        return self._color
    
    @color.setter
    def color(self, value: Color | int | str | tuple | None):
        if isinstance(value, Color) or value is None:
            self._color = value
        elif value is ...:
            self._color = Color.random()
        else:
            self._color = Color(value)