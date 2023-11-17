from piligraphs import CircleGraph, CircleGraphItem

graph = CircleGraph(radius=1000, emboss=100)
graph.add_items(
    CircleGraphItem(name="", color="220000", value=6),
    CircleGraphItem(name="", color="002200", value=39),
    CircleGraphItem(name="", color="000022", value=25),
    
)

fg = CircleGraph(radius=800, emboss=100)
fg.add_items(
    CircleGraphItem(name="", color="ff0000", value=2),
    CircleGraphItem(name="", color="ee0000", value=2),
    CircleGraphItem(name="", color="dd0000", value=2),

    CircleGraphItem(name="", color="00ff00", value=10),
    CircleGraphItem(name="", color="00ee00", value=9),
    CircleGraphItem(name="", color="00dd00", value=20),

    CircleGraphItem(name="", color="0000ff", value=5),
    CircleGraphItem(name="", color="0000ee", value=14),
    CircleGraphItem(name="", color="0000dd", value=6),
)

img = graph.draw()
fgimg = fg.draw()
img.paste(fgimg, (200, 200), fgimg)
img.show()