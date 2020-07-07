from PIL import Image, ImageChops, ImageOps
import glob
import numpy as np
from os import listdir,walk
import os
import shutil

TOTAL_SIZE = 300
BASE_SIZE = int(TOTAL_SIZE*0.70)
BORDER_SIZE = int(TOTAL_SIZE*0.15) # BORDER SIZE REFERS TO TWO SIDES,
# CURRENT SETTING IS 0.7 + 0.15 * 2 Sides for an Image

# Trims the Image
def trim(image):
    inverted = ImageOps.invert(image.convert("RGB"))
    return image.crop(inverted.getbbox())

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
    # PRINT TO TEXT FILE
    log = open('log.txt', 'w')

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
            try:
                print("Processing:{} from {}".format(imageName,path))
                lastDotIndex = imageName.rfind(".")
                [imageName,imageFormat] = [imageName[0:lastDotIndex],imageName[lastDotIndex+1:]]
                image = Image.open("{}/{}.{}".format(path,imageName,imageFormat)).convert("RGBA")
                iccProfile = image.info.get("icc_profile",'')

                image = trim(image)
                image = resizeToSizePreserveRatio(image,BASE_SIZE)

                # image = removeWhiteBackground(image)
                # PADDING ADDITION
                imageFirstPixelColor = image.getpixel((0, 0))
                imageFirstPixelColor = (255,255,255) if (imageFirstPixelColor!=(0,0,0,255)) else imageFirstPixelColor


                image = addPadding(image,BORDER_SIZE,imageFirstPixelColor)

                # MAKE SQUARE
                image = makeSquare(image,imageFirstPixelColor)

                image.save("outputNormal{}/{}.{}".format(outputPath,imageName,imageFormat),"PNG",icc_profile=iccProfile)
                if (imageFormat=="jpg"):
                    image.save("outputTransparent{}/{}.{}".format(outputPath,imageName,imageFormat),"PNG",icc_profile=iccProfile)
                else:
                    os.popen("magick convert outputNormal{}/{}.{} -fuzz 5% -fill none -draw \"color 0,0 floodfill\" -transparent none outputTransparent{}/{}.{}".format(outputPath,imageName,imageFormat,outputPath,imageName,imageFormat))
            except Exception as err:
                log.write("Error with {}.{} \n".format(imageName,imageFormat))
                print(err)

if __name__ == "__main__":
    main()
    print("FINISHED")
    # os.system("start.sh")

