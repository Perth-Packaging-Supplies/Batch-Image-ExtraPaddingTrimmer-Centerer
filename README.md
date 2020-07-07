# Batch-Image-ExtraPaddingTrimmer+Centerer
Video Documentation: https://youtu.be/hZQocChysnU

# What is it?
This program is mainly used for digital marketting. This script will do the following for a batch of pictures:
1. Remove extra padding on the picture, by cropping the background up to the product box.
2. Resize the picture to a specific proportionate size
3. Add padding that is equal in all side to ensure that the product will always be at the center of the product. The color of the padding the same as the first pixel encountered in the top-left corner.

*Note that you could put your folder of pictures inside the input folder, and it will do the instructions of the script FOR ALL PICTURES, FOR ALL FOLDERS INSIDE OF FOLDERS. The output will be the adjusted pictures in the same directory structure as the input folder.*

For example: If you have a folder structure:
```
input >> folder1 >> img.png
                 >> img2.jpg
      >> folder2 >> abc.jpg
```
The output will be similar
```
output >> folder1 >> img.png
                  >> img2.jpg
       >> folder2 >> abc.jpg
      
outputTransparent >> folder1 >> img.png
                             >> img2.jpg
                  >> folder2 >> abc.jpg
```

This program is only tested for `jpg` and `png`. You can only convert png to transparent, but the jpg will be copied over. If there are any problems in the conversion, a file called `log.txt` is created that will record the encounter.

# Requirements:
1. Python installed. More information can be found [here](https://www.python.org/downloads/)
2. (Optional - if you want transparent pictures) Magick installed. More information can be [here](http://www.besavvy.com/documentation/4-5/Editor/031350_installimgk.htm). Currently there is a code that I wrote for removing the background, but it doesn't seem to perform as well as Magick
3. Pil, just incase the standard python does not have this. This can be installed by typing `pip install pillow`


