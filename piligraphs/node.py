from pinkie import Color

from .utils import get_color


class Node:
    """Class representing a graph node."""

    def __init__(
        self,
        *,
        weight: int | float = 1,
        color: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...
    ) -> None:
        self.weight = weight
        self.color = get_color(color)
    