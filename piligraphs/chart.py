from .graph import Graph
from .node import Node


class Chart(Graph):
    def __init__(self) -> None:
        self.nodes: list[Node] = []
    
    def add_node(self, node: Node, /) -> None:
        """
        Add a node to the chart.

        Attributes
        ----------
        node: `Node`
            Node to add.
        """
        if not isinstance(node, Node):
            raise TypeError(f"nodes must be instances of '{Node.__name__}', not {type(node).__name__}")
        
        self.nodes.append(node)
        
    def add_nodes(self, *nodes: Node) -> None:
        """
        Add all nodes to the chart.

        Attributes
        ----------
        nodes: `Node`
            Nodes to add.
        """
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node: Node, /) -> None:
        """
        Remove a node from the chart.

        Attributes
        ----------
        node: `Node`
            Node to remove.
        """
        self.nodes.remove(node)

    def remove_nodes(self, *nodes: Node) -> None:
        """
        Remove all nodes from the chart.

        Attributes
        ----------
        nodes: `Node`
            Nodes to remove.
        """
        for node in nodes:
            self.remove_node(node)
