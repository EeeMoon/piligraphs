from .color import Color


class GraphItem:
    """Class representing Graph item."""

    def __init__(self,
                 *,
                 name: str, 
                 color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int],
                 value: int | float) -> None:
        self.name: str = name
        self.color: Color = color if isinstance(color, Color) else Color(color)
        self.value: int | float = value
