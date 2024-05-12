from pinkie import Color

from .utils import get_color


class GraphItem:
    """Class representing a graph item."""

    def __init__(
        self,
        *,
        color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        weight: int | float = 1
    ) -> None:
        self.color = get_color(color)
        self.weight = weight
    