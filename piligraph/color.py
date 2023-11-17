from .utils import hex_to_rgb, int_to_rgb, rgb_to_hex, rgb_to_int


class Color:
    """Class representing a 0-255 range color."""

    def __init__(self,
                 color: int | str | tuple[int, int, int] | tuple[int, int, int, int],
                 alpha: int = None) -> None:
        """
        Constructs `Color` from value.

        Attributes
        ----------
        color: `int` | `str` | `tuple[int, int, int]` | `tuple[int, int, int, int]`
            Color value. Can be `HEX`, `RGB`, `RGBA` or color number.
        """
        self._alpha = 255

        if isinstance(color, str):
            color = hex_to_rgb(color.removeprefix("#"))
        elif isinstance(color, int):
            color = int_to_rgb(color)
        elif isinstance(color, tuple) and len(color) == 4:
            if alpha is None:
                self._alpha = color[3]
            color = color[:3]

        self._color: tuple[int, int, int] = color

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Get the color in `RGB` format."""
        return self._color

    @property
    def hex(self) -> str:
        """Get the color in `HEX` format."""
        return rgb_to_hex(self._color)
    
    @property
    def num(self) -> int:
        """Get the color as number."""
        return rgb_to_int(self._color)
    
    @property
    def alpha(self) -> int:
        """Get the color alpha."""
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: int):
        self._alpha = value

    

