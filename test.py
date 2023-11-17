from piligraph import CircleGraph, CircleGraphItem

graph = CircleGraph(radius=1000, thickness=500, emboss=50, angle=100)
graph.add_items(
    CircleGraphItem(name="", color="00ff00", value=3),
    CircleGraphItem(name="", color="0000ff", value=10),
    CircleGraphItem(name="", color="0f0f00", value=25),
    CircleGraphItem(name="", color="00f00f", value=39),
    CircleGraphItem(name="", color="ff0000", value=40),
)
