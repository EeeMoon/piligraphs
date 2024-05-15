import math
from PIL import Image
from piligraphs import FuncGraph


# define a base image
image = Image.new('RGBA', (1000, 1000))

# define a graph
graph = FuncGraph(
    image.size,
    func=lambda x: x**2, # quadratic function
    thickness=10,
    outline="4e9f2b",
    res=(20, 20), # x and y will be in range [-20; 20]
    npoints=image.width // 5
)

# draw the graph
img = graph.draw()
image.paste(img, (0, 0), img)

# add another functions
graph.func = math.sin
graph.outline = "4961bd"
img = graph.draw()
image.paste(img, (0, 0), img)

graph.func = lambda x: x**3
graph.outline = "d2702c"
img = graph.draw()
image.paste(img, (0, 0), img)

# preview
image.show()