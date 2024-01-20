from PIL import Image
import numpy as np

PATH = "./assets/blanktrash.png"
WHITE = (255, 255, 255)

def pixel_distance(pixel1: tuple, pixel2: tuple) -> float:
    dist_sqr = 0
    for i in range(3):
        dist_sqr += (pixel1[i] - pixel2[i]) ** 2
    return np.sqrt(dist_sqr)

def reddify_image(path: str, amount: int = 50, white_threshold: float = 50):
    img = Image.open(PATH)
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0 or pixel_distance(pixel, WHITE) < white_threshold: continue
            newPixel = (pixel[0] + amount - 25, pixel[1] - amount, pixel[2] - amount - 25, pixel[3])
            img.putpixel((x, y), newPixel)
    img.save(f"./assets/red.png")

def greenify_image(path: str, amount: int = 50, white_threshold: float = 50):
    img = Image.open(PATH)
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0 or pixel_distance(pixel, WHITE) < white_threshold: continue
            newPixel = (pixel[0] - amount - 50, pixel[1] + amount - 50, pixel[2] - amount - 50, pixel[3])
            img.putpixel((x, y), newPixel)
    img.save(f"./assets/green.png")

def blackify_image(path: str, amount: int = 50, white_threshold: float = 50):
    img = Image.open(PATH)
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0 or pixel_distance(pixel, WHITE) < white_threshold: continue
            newPixel = (pixel[0] - amount, pixel[0] - amount, pixel[0] - amount, pixel[3])
            img.putpixel((x, y), newPixel)
    img.save(f"./assets/black.png")

def blueify_image(path: str, amount: int = 50, white_threshold: float = 50):
    img = Image.open(PATH)
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0 or pixel_distance(pixel, WHITE) < white_threshold: continue
            newPixel = (pixel[0] - amount, pixel[1] - amount, pixel[2] - amount, pixel[3])
            img.putpixel((x, y), newPixel)
    img.save(f"./assets/blue.png")

if __name__ == "__main__":
    reddify_image(PATH, 130, 100)
    greenify_image(PATH, 80, 90)
    blackify_image(PATH, 50, 100)
    blueify_image(PATH, 50, 100)