import random
import time
from PIL import Image

from piligraphs import LineChart, RadarChart, PieChart, GraphItem


# define variables
margin = 50
items = [GraphItem(weight=random.randint(1, 5)) for _ in range(20)]
graphs = []


# create graphs
linechart = LineChart(
    size=(2000, 1000),
    thickness=10,
    point_width=20,
    num_points=len(items) * 10,
    interpol='cubic',
    min_height=100
)
linechart.add_items(*items)
graphs.append(linechart)


radarchart = RadarChart(
    radius=500,
    thickness=10,
    point_width=20,
    num_points=len(items) * 10,
    interpol='cubic',
    min_radius=100
)
radarchart.add_items(*items)
graphs.append(radarchart)


piechart = PieChart(
    radius=500, 
    width=300,
    emboss=50,
    space_between=10)
piechart.add_items(*items)
graphs.append(piechart)


def timer(func, name: str):
    start = time.time()
    res = func()
    end = time.time()
    print(f"Executed '{name}' in {end - start} seconds")
    return res


# display graphs
graph_images: list[Image.Image] = [
    timer(lambda: graph.draw(), f"{type(graph).__name__}.draw()") for graph in graphs]
size = (
    sum((g.width for g in graph_images)) + margin * (len(graph_images) + 1), 
    max((g.height for g in graph_images)) + margin * 2
)
image = Image.new('RGBA', size, (0, 0, 0, 0))

x = margin
for graph in graph_images:
    image.paste(graph, (x, margin), graph)
    x += graph.width + margin

image.show("All graphs with the same data")
