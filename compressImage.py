import os
from PIL import Image
import pillow_avif
import torch
from piq import DISTS
from skimage.io import imread
import uuid

def compressImageToSize(pathRoot, outputFolderName, file, desiredSize, step, format, extension):
    # instantiate class
    class imageInfo:
        quality = [50, 50, 50] # an array of the past 3 qualities of ouputs
        size = None # the size of the ouput images
        sizeDelta = None # the difference between the ouput size and the desired size
        path = "" # image path
    imageSizeEqual = False
    counter = 0

    outputPath = os.path.join(pathRoot + outputFolderName + "/", str(desiredSize/1000) + "kb" + "/")
    try: 
        os.mkdir(outputPath)
    except:
        print("directory already exists")

    os.chdir(pathRoot)
    while not imageSizeEqual: 
        # compress the image using the desired format and extension, save to desired location
        with Image.open(file) as im:
            im.save(outputPath + "/" + file + extension, format, quality=imageInfo.quality[counter%3])
            imageInfo.path = (outputPath + "/" + file + extension)
        imageInfo.size = os.path.getsize(imageInfo.path) 

        # check if image is below, above or equal to the desired size and adjust quality accordingly
        if imageInfo.size < desiredSize:
            imageInfo.quality[counter%3] = imageInfo.quality[counter%3-1] + step
        elif imageInfo.size > desiredSize:
            imageInfo.quality[counter%3] = imageInfo.quality[counter%3-1] - step
        else:
            imageSizeEqual = True
        print(imageInfo.quality)
        
        # set flag to true if the quality of the compressions is bouncing between two values
        if imageInfo.quality[counter%3] == imageInfo.quality[counter%3-2]:
            imageSizeEqual = True

        if ((imageInfo.quality[counter%3] == 0) or (imageInfo.quality[counter%3] == 100)):
            imageSizeEqual = True

        counter += 1

    # calculate the delta
    imageInfo.sizeDelta = abs(desiredSize - imageInfo.size)
    # return the image info
    return imageInfo

## takes in BMP image file paths and outputs quality
def calcImageQuality(imgXPath, imgYPath):
    imgX = torch.tensor(imread(imgXPath)).permute(2, 0, 1)[None, ...] / 255.
    imgY = torch.tensor(imread(imgYPath)).permute(2, 0, 1)[None, ...] / 255.
    dists_loss = DISTS(reduction='none')(imgX, imgY)
    return(f"{dists_loss.item():0.4f}")

def convertBackToBMP(imageInfo, tmpFolderName):
    name = str(uuid.uuid4())
    with Image.open(imageInfo.path) as im:
        im.save(tmpFolderName + "/" + name + ".bmp", "BMP")
        return(tmpFolderName + "/" + name + ".bmp")
    
def getCompressedQualityOfImage(file, pathRoot, outputFolderName, tmpFolderName, fileSize, qualityStep, format, extension):
    return calcImageQuality(convertBackToBMP(compressImageToSize(pathRoot, outputFolderName, file, fileSize, qualityStep, format, extension), tmpFolderName), (file))