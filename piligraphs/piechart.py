from PIL import Image, ImageDraw

from .chart import Chart
from .utils import circle_xy, limit


class PieChart(Chart):
    """Class representing a pie chart."""

    def __init__(
        self,
        radius: int,
        *,
        thickness: int = 0,
        angle: int = 0,
        emboss: int = 0,
        gap: int = 0
    ) -> None:
        """
        Attributes
        ----------
        radius: `int`
            Radius of the chart circle.
        thickness: `int`
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
        self.thickness = thickness
        self.angle = angle
        self.emboss = emboss
        self.gap = gap

    def draw(self) -> Image.Image:
        radius = self.radius
        w = radius * 2
        image = Image.new('RGBA', (w, w))
        num_nodes = len(self.nodes)

        if num_nodes == 0:
            return image
        
        draw = ImageDraw.Draw(image)

        weights = [node.weight for node in self.nodes]
        total_weight = sum(weights)
        start_angle = self.angle
        emboss = self.emboss
        gap = self.gap
        clear_co = (0, 0, 0, 0)
        eq_angle = 360 / num_nodes
        w_angle = 360 / total_weight

        offsets = limit(
            weights, 
            0 if emboss < 0 else abs(emboss), 
            abs(emboss) if emboss < 0 else 0
        )

        for num, node in enumerate(self.nodes):
            offset = offsets[num]
            angle = eq_angle if total_weight == 0 else w_angle * node.weight 
            end_angle = start_angle + angle

            if node.color is not None:
                draw.pieslice(
                    (
                        (offset, offset), 
                        (w - offset, w - offset)
                    ),
                    start_angle, 
                    end_angle,
                    fill=node.color.rgba,
                    width=0
                )
                
                if gap > 0 and num:
                    draw.line(
                        (
                            (radius, radius), 
                            circle_xy(radius, radius, start_angle)
                        ),
                        fill=clear_co, 
                        width=gap
                    )
                
                if self.thickness > 0:
                    l_space = self.thickness - offset
                    r_space = w - l_space

                    draw.pieslice(
                        ((l_space, l_space), (r_space, r_space)),
                        start_angle,
                        end_angle,
                        fill=clear_co,
                        width=0
                    )

            start_angle += angle

        if gap:
            draw.line(
                (
                    (radius, radius), 
                    circle_xy(radius, radius, start_angle)
                ),
                fill=clear_co, 
                width=gap
            )
            
            half_gap = gap / 2

            draw.ellipse(
                (
                    (radius - half_gap, radius - half_gap), 
                    (radius + half_gap, radius + half_gap)
                ),
                fill=clear_co, 
                width=0
            )
            
        return image
