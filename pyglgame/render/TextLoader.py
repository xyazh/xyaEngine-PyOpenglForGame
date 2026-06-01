from PIL import ImageFont, ImageDraw, Image
from .Texture import Texture


class TextLoader:

    def __init__(self, font_path: str, font_size: int):
        self.font = ImageFont.truetype(font_path, font_size)

    def createTexture(self,
                      text: str,
                      color=(255, 255, 255, 255),
                      bg_color=(0, 0, 0, 0),
                      padding=4):
        bbox = self.font.getbbox(text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        img = Image.new(
            "RGBA",
            (width + padding * 2, height + padding * 2),
            bg_color
        )
        draw = ImageDraw.Draw(img)
        draw.text(
            (padding - bbox[0], padding - bbox[1]),
            text,
            fill=color,
            font=self.font
        )
        return Texture.createDataTexture(
            img.tobytes(),
            img.width,
            img.height
        )