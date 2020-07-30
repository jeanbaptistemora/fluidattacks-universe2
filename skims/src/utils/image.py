# Third party libraries
from PIL import (
    Image,
)


def blocking_clarify(image: Image, ratio: float) -> Image:
    image_mask: Image = image.convert('L')
    image_mask_pixels = image_mask.load()

    image_width, image_height = image_mask.size

    for i in range(image_width):
        for j in range(image_height):
            if image_mask_pixels[i, j]:
                image_mask_pixels[i, j] = int(ratio * 0xff)

    image.putalpha(image_mask)

    return image
