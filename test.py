from PIL import Image, ImageChops, ImageOps
# input\products\__thumbnails\01BG2TTK_png.webp

path = 'input\\products\\__thumbnails\\01BG2TTK_png.webp'
image = Image.open(path)
image.save("test.webp","PNG")
image.save("test.png","PNG")