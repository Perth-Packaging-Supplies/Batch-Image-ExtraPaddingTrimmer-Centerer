from PIL import Image, ImageChops, ImageOps
import glob
import numpy as np
from os import listdir,walk
import os
import shutil

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
    imageWidth,imageHeight = image.size

    maxImageDimension = max(imageHeight,imageWidth)
    percentDiff = baseSize/maxImageDimension

    # The Image Is Portrait
    if(maxImageDimension==imageHeight):
        otherImageDimension = int(float(imageWidth)*float(percentDiff))
        return image.resize((otherImageDimension,baseSize),Image.ANTIALIAS)

    #The Image is LandScape
    else:
        otherImageDimension = int(float(imageHeight)*float(percentDiff))
        return image.resize((baseSize,otherImageDimension),Image.ANTIALIAS)

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

def addPadding(image,borderSize,fillColor="white"):
    return ImageOps.expand(image,border=borderSize,fill=fillColor)

def makeSquare(image,fillColor="white"):
    width,height = image.size
    size = max(width,height)
    newImage = Image.new("RGBA",(size,size),fillColor)
    newImage.paste(image, (int((size - width) / 2), int((size - height) / 2)))
    return newImage

def deleteFolderInPath(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

def main():
    #DELETE FILES IN OUTPUT FOLDERS
    deleteFolderInPath("outputNormal")
    deleteFolderInPath("outputTransparent")

    allDirectories =  walk("input")

    for path,directories,imageNames in allDirectories:
        path = path.replace("\\","/")
        outputPath = path[5:]

        try:
            os.mkdir("outputNormal{}".format(outputPath))
            os.mkdir("outputTransparent{}".format(outputPath))
        except:
            print()

        for imageName in imageNames:
            imageName,imageFormat = imageName.split(".")
            image = Image.open("{}/{}.{}".format(path,imageName,imageFormat))
            image = trim(image)

            TOTAL_SIZE = 300
            BASE_SIZE = int(TOTAL_SIZE*0.70)
            image = resizeToSizePreserveRatio(image,BASE_SIZE)

            # image = removeWhiteBackground(image)
            # PADDING ADDITION
            BORDER_SIZE = int(TOTAL_SIZE*0.15)
            image = addPadding(image,BORDER_SIZE)

            # MAKE SQUARe
            image = makeSquare(image)

            #REMOVE "input" in the pathname

            image.save("outputNormal{}/{}.{}".format(outputPath,imageName,imageFormat),"PNG")
            os.popen("magick convert outputNormal{}/{}.{} -fuzz 5% -fill magenta -draw \"color 0,0 floodfill\" -transparent magenta outputTransparent{}/{}.{}".format(outputPath,imageName,imageFormat,outputPath,imageName,imageFormat))

if __name__ == "__main__":
    main()
    # os.system("start.sh")

