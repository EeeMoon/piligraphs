from PIL import Image


class Chart:
    def draw(self) -> Image.Image:
        """
        Draw the chart.
        """
        raise NotImplementedError()
