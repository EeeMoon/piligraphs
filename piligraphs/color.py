class Color:
    """Class representing a 8-bit color."""
    def __init__(self,
                 color: int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = None,
                 /,
                 alpha: int | None = None) -> None:
        """
        Constructs `Color` from value.

        Attributes
        ----------
        color: `int` | `str` | `tuple[int, int, int]` | `tuple[int, int, int, int]`
            Color value. Can be `HEX`, `RGB`, `RGBA` or color number.
            If `None`, sets to black transparent color.
        """        
        self.alpha = 255

        if isinstance(color, str):
            from .utils import hex_to_rgb
            color = hex_to_rgb(color.removeprefix("#"))
        elif isinstance(color, int):
            from .utils import num_to_rgb
            color = num_to_rgb(color)
        elif isinstance(color, tuple) and len(color) == 4:
            if alpha is None:
                self.alpha = color[3]
            color = color[:3]
        elif color is None:
            self.alpha = 0
            color = (0, 0, 0)
        else:
            raise ValueError("invalid color value")
    
        self._rgb: tuple[int, int, int] = color

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Get the color in `RGB` format."""
        return self._rgb
    
    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """Get the color in `RGBA` format."""
        return self._rgb + (self._alpha,)

    @property
    def hex(self) -> str:
        """Get the color in `HEX` format."""
        from .utils import rgb_to_hex
        return rgb_to_hex(self._rgb)
    
    @property
    def number(self) -> int:
        """Get the color as number."""
        from .utils import rgb_to_num
        return rgb_to_num(self._rgb)
    
    @property
    def alpha(self) -> int:
        """Get the color alpha."""
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: int):
        self._alpha = value