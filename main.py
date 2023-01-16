from compressImage import getCompressedQualityOfImage
import csv
import os, glob

pathRoot = "/Users/william_bradshaw23/Documents/ee/code/images/"
outputFolderName = "output"
tmpFolderName = "tmp"
fileSizes = [50_000, 100_000, 150_000, 200_000, 250_000, 300_000]
formats = [["JPEG", ".jpeg"], ["AVIF", ".avif"]]

os.chdir(pathRoot)
for file in glob.glob("*.bmp"):
    with open(file + ".csv", 'w') as csvFile:
        header = []
        for format in formats:
            header.append(format[0])
            header.extend("" for x in range(len(fileSizes)-1))
        csvRows = [header, fileSizes]
        csvWriter = csv.writer(csvFile)

        row = []
        for fileSize in fileSizes:
            for format in formats:
                row.append(getCompressedQualityOfImage(file, pathRoot, outputFolderName, tmpFolderName, fileSize, 1, format[0], format[1]))
        print(row)

        csvRows.append(row)
        csvWriter.writerows(csvRows)







