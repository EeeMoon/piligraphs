class Size:
    def __init__(self, size: tuple[int, int]) -> None:
        if (len(size) != 2
            or not all((isinstance(i, int) for i in size))):
            raise ValueError("'size' must be iterable containing 2 integers")
       
        self._size: tuple[int, int] = size
    
    def __getitem__(self, key: int):
        return self._size[key]
    
    def __setitem__(self, key: int, value: int):
        self._validate(value, 'value')
        self._size[key] = value

    @staticmethod
    def _validate(value: int, name: str) -> None:
        if (not isinstance(value, int)
            or value < 0):
            raise ValueError(f"'{name}' must be greater than 0")
    
    @property
    def width(self):
        """Width."""
        return self._size[0]
    
    @width.setter
    def width(self, value: int):
        self._validate(value, 'width')
        self._size[0] = value

    @property
    def height(self):
        """Height."""
        return self._size[1]
    
    @height.setter
    def height(self, value: int):
        self._validate(value, 'height')
        self._size[1] = value

    