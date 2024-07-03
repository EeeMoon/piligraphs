from PIL import Image


from .node import Node


class Graph:
    def draw(self) -> Image.Image:
        """Draw the graph."""
        raise NotImplementedError()


class NodeGraph(Graph):
    def __init__(self) -> None:
        self._nodes: list[Node] = []

    @property
    def nodes(self) -> list[Node]:
        return self._nodes
        
    def add_nodes(self, *nodes: Node) -> None:
        """
        Add all nodes to the graph.

        Parameters
        ----------
        nodes: `Node`
            Nodes to add.
        """
        for node in nodes:
            if not isinstance(node, Node):
                raise TypeError(
                    f"Node must be instance of '{Node.__name__}',"
                    f" not {type(node).__name__}"
                )
            
            self.add_node(node)

    def remove_nodes(self, *nodes: Node) -> None:
        """
        Remove all nodes from the graph.

        Parameters
        ----------
        nodes: `Node`
            Nodes to remove.
        """
        for node in nodes:
            self.remove_node(node)
