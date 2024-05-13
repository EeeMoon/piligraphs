import random
from PIL import Image
from piligraphs import BaseChart, LineGraph, RadarChart, PieChart, ChartItem


# define variables
margin = 50
items = [ChartItem(
    color=(
        random.randint(128, 216), 
        random.randint(128, 216), 
        random.randint(128, 216), 
        256
    ), 
    weight=random.randint(1, 5)) for _ in range(12)
]
graphs: list[BaseChart] = []


# create graphs
linechart = LineGraph(
    size=(2000, 1000),
    thickness=10,
    fill=(23, 100, 231, 156),
    outline=(45, 143, 197, 256),
    pwidth=20,
    onlysrc=True,
    npoints=len(items) * 5,
    interp='cubic',
    minh=100
)
linechart.add_nodes(*items)
graphs.append(linechart)


radarchart = RadarChart(
    radius=500,
    thickness=10,
    fill=(167, 33, 242, 156),
    outline=(189, 12, 234, 256),
    pwidth=20,
    onlysrc=True,
    npoints=len(items),
    interp='cubic',
    minr=100
)
radarchart.add_items(*items)
graphs.append(radarchart)


piechart = PieChart(
    radius=500, 
    thickness=300,
    emboss=50,
    gap=10
)
piechart.add_nodes(*items)
graphs.append(piechart)


# draw graphs
images  = [g.draw() for g in graphs]
size = (
    sum((g.width for g in images)) + margin * (len(images) + 1), 
    max((g.height for g in images)) + margin * 2
)
image = Image.new('RGBA', size, (0, 0, 0, 0))

x = margin
for img in images:
    image.paste(img, (x, margin), img)
    x += img.width + margin

image.show("All graphs with the same data")