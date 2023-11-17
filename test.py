from piligraphs import CircleGraph, CircleGraphItem

graph = CircleGraph(radius=2000, emboss=200)
graph.add_items(
    CircleGraphItem(name="", color="00ff00", value=3),
    CircleGraphItem(name="", color="00f00f", value=39),
    CircleGraphItem(name="", color="0f0f00", value=25),
    CircleGraphItem(name="", color="0000ff", value=10),
    CircleGraphItem(name="", color="ff0000", value=40),
)

img = graph.draw()
img.show()