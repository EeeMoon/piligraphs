from PIL import Image

from .item import GraphItem


class BaseGraph:
    def __init__(self) -> None:
        self.items: list[GraphItem] = []
    
    def add_item(self, item: GraphItem, /) -> None:
        """
        Add an item to the graph.

        Attributes
        ----------
        item: `GraphItem`
            Item to add.
        """
        if not isinstance(item, GraphItem):
            raise TypeError(f"items must be instances of '{GraphItem.__name__}', not {type(item).__name__}")
        
        self.items.append(item)
        
    def add_items(self, *items: GraphItem) -> None:
        """
        Add all items to the graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to add.
        """
        for item in items:
            self.add_item(item)

    def remove_item(self, item: GraphItem, /) -> None:
        """
        Remove the item from the graph.

        Attributes
        ----------
        item: `GraphItem`
            Item to remove.
        """
        self.items.remove(item)

    def remove_items(self, *items: GraphItem) -> None:
        """
        Remove items from graph.

        Attributes
        ----------
        items: `GraphItem`
            Items to remove.
        """
        for item in items:
            self.remove_item(item)

    def draw(self) -> Image.Image:
        """
        Draw the graph.
        """
        raise NotImplementedError()
