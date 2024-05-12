# piligraphs
[![pypi](https://img.shields.io/pypi/v/piligraphs)](https://pypi.org/project/piligraphs)
[![python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads)
[![CodeFactor](https://www.codefactor.io/repository/github/eeemoon/piligraphs/badge)](https://www.codefactor.io/repository/github/eeemoon/piligraphs)
[![BuyMeACoffee](https://img.shields.io/badge/support-yellow)](https://www.buymeacoffee.com/eeemoon)

A [Pillow](https://github.com/python-pillow/Pillow) extension for drawing graphs and charts.

![](examples/images/allgraphs.png)

## Installation
To install this module, run the following command:
```
pip install piligraphs
```

## Example usage
Creating a line chart:
```python
import random
from piligraphs import LineChart, GraphItem

# define items
items = [
    GraphItem(weight=random.randint(1, 7)) for _ in range(10)
]

# create a LineChart
linechart = LineChart(
    size=(1200, 300),
    thickness=8,
    fill=(243, 14, 95, 156),
    outline=(194, 43, 132, 256),
    pwidth=15,
    onlysrc=True,
    npoints=len(items) * 8,
    interp='cubic'
)

# add items
linechart.add_items(*items)

# draw graph
image = linechart.draw()
image.show()
```
Result:
![](examples/images/linegraph.png)

You can find more examples [here.](examples/)
