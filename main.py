from PIL import Image, ImageChops
import glob
import numpy as np

# Trims the Image
def trim(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)

# Resizes the image
def resizeToSizePreserveRatio(image,baseSize):
    imageWidth = image.size[0]
    imageHeight = image.size[1]

    maxImageDimension = max(imageHeight,imageWidth)
    percentDiff = BASE_SIZE/maxImageDimension

    # The Image Is Portrait
    if(maxImageDimension==imageHeight):
        otherImageDimension = int(float(imageWidth)*float(percentDiff))
        return image.resize((otherImageDimension,BASE_SIZE),Image.ANTIALIAS)

    #The Image is LandScape
    else:
        otherImageDimension = int(float(imageHeight)*float(percentDiff))
        return image.resize((BASE_SIZE,otherImageDimension),Image.ANTIALIAS)

def removeWhiteBackground(image):
    image = image.convert("RGBA")
    pixdata = image.load()

    THRESHOLD=100
    DISTANCE=5

    # np.asarray(img) is read only. Wrap it in np.array to make it modifiable.
    imageArray=np.array(np.asarray(image))

    r,g,b,a=np.rollaxis(imageArray,axis=-1)
    mask=((r>THRESHOLD)
        & (g>THRESHOLD)
        & (b>THRESHOLD)
        & (np.abs(r-g)<DISTANCE)
        & (np.abs(r-b)<DISTANCE)
        & (np.abs(g-b)<DISTANCE)
        )

    imageArray[mask,3]=0
    image = Image.fromarray(imageArray,mode='RGBA')

    return image

image = Image.open("input/test.png")
image = trim(image)

BASE_SIZE = 300
image = resizeToSizePreserveRatio(image,BASE_SIZE)

image = removeWhiteBackground(image)

image.save("output/test.png","PNG")