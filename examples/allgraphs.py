import random
from PIL import Image, ImageDraw

from piligraphs import (LineChart, RadarChart, PieChart, 
                        GraphItem, Interpolation)


graphs = []
items = [GraphItem(weight=random.randint(1, 10)) for _ in range(20)]


linechart = LineChart(
    size=(2000, 1000),
    thickness=10,
    point_width=20,
    num_points=len(items) * 10,
    interpol=Interpolation.CUBIC,
    min_height=50
)
linechart.add_items(*items)
graphs.append(linechart)


radarchart = RadarChart(
    radius=500,
    thickness=10,
    point_width=20,
    num_points=len(items) * 10,
    interpol=Interpolation.CUBIC,
    min_radius=50
)
radarchart.add_items(*items)
graphs.append(radarchart)


piechart = PieChart(
    radius=1000, 
    width=500,
    emboss=100,
    space_between=10)
piechart.add_items(*items)
graphs.append(piechart)


graph_images: list[Image.Image] = [graph.draw() for graph in graphs]

size = (
    sum((g.width for g in graph_images)),
    max((g.height for g in graph_images))
)

image = Image.new('RGBA', size, (0, 0, 0, 255))
draw = ImageDraw.Draw(image)
x = 0

for graph in graph_images:
    image.paste(graph)
    x += graph.width

image.show()
    



