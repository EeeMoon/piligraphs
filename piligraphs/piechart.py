from PIL import Image, ImageDraw

from .basegraph import BaseGraph
from .utils import circle_xy, limit


class PieChart(BaseGraph):
    """Class representing a Pie Chart."""

    def __init__(
        self,
        radius: int,
        *,
        width: int = 0,
        angle: int = 0,
        emboss: int = 0,
        gap: int = 0
    ) -> None:
        """
        Attributes
        ----------
        radius: `int`
            Radius of the chart circle.
        width: `int`
            If None, graph will be pie-shaped.
            Otherwise, graph will be donut-shaped with specified thickness.
        angle: `int`
            Start angle of the chart.
        emboss: `int`
            Difference between the largest and smallest slice.
            If < 0, slice size inverts (bigger value = smaller radius).
        gap: `int`
            Space between the pie slices.
        """
        super().__init__()

        self.radius = radius
        self.width = width
        self.angle = angle
        self.emboss = emboss
        self.gap = gap

    def draw(self) -> Image.Image:
        w = self.radius * 2
        image = Image.new('RGBA', (w, w))
        num_items = len(self.items)

        if num_items == 0:
            return image
        
        weights = [item.weight for item in self.items]
        total_weight = sum(weights)
        start_angle = self.angle
        width = self.width
        emboss = self.emboss
        clear_co = (0, 0, 0, 0)
        template = image.copy()

        offsets = limit(
            weights, 
            0 if emboss < 0 else abs(emboss), 
            abs(emboss) if emboss < 0 else 0
        )

        for i, item in enumerate(self.items):
            img = template.copy()
            draw = ImageDraw.Draw(img)
            offset = offsets[i]

            if total_weight == 0: 
                angle = 360 / num_items
            else:
                angle = 360 * item.weight / total_weight

            if item.color is not None:
                draw.pieslice(
                    (
                        (offset, offset), 
                        (img.width - offset,) * 2
                    ),
                    start_angle, 
                    start_angle + angle,
                    fill=item.color.rgba)
                
                if self.gap > 0:
                    draw.line(
                        (
                            (self.radius, self.radius), 
                            circle_xy(self.radius, self.radius, start_angle + angle)
                        ),
                        fill=clear_co, 
                        width=self.gap
                    )
                    draw.line(
                        (
                            (self.radius, self.radius), 
                            circle_xy(self.radius, self.radius, start_angle)
                        ),
                        fill=clear_co, 
                        width=self.gap
                    )
                    draw.ellipse(
                        (
                            (self.radius - self.gap / 2,) * 2, 
                            (self.radius + self.gap / 2,) * 2
                        ),
                        fill=clear_co, 
                        width=0
                    )
            
                if width > 0:
                    draw.ellipse(
                        (
                            (width - offset,) * 2, 
                            (self.radius * 2 - width + offset,) * 2
                        ),
                        fill=clear_co
                    )
            
                image.alpha_composite(img)

            start_angle += angle

        return image


    