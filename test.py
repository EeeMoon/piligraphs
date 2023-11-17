from piligraph import CircleGraph, GraphItem

graph = CircleGraph(radius=1000, thickness=500, emboss=-120, angle=100)
graph.add_items(GraphItem(name="", color="00ff00", value=3))
graph.add_items(GraphItem(name="", color="0000ff", value=10))
graph.add_items(GraphItem(name="", color="0f0f00", value=25))
graph.add_items(GraphItem(name="", color="00f00f", value=39))
graph.add_items(GraphItem(name="", color="ff0000", value=40))

graph.draw().show()