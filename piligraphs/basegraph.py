from PIL import Image

from .item import GraphItem


class BaseGraph:
    def __init__(self) -> None:
        self._items: list[GraphItem] = []
        
    @property
    def items(self) -> list[GraphItem]:
        """Graph items."""
        return self._items.copy()
        
    def add_items(self, *items: GraphItem) -> None:
        """
        Add items to graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to add.

        Raises
        ------
        `ValueError` if item is not of correct type.
        """
        for item in items:
            if not isinstance(item, GraphItem):
                raise ValueError(f"items must be instances of '{GraphItem.__name__}', not {type(item).__name__}")
            self._items.append(item)

    def remove_items(self, *items: GraphItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to remove.

        Raises
        ------
        `ValueError` if item is not present.
        """
        for item in items:
            self._items.remove(item)

    def draw(self) -> Image.Image:
        """
        Draw a graph.
        """
        raise NotImplementedError()
