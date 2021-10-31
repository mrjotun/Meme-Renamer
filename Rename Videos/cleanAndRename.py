import sys, getopt, os
import subprocess
import glob
import re
from pathlib import Path

def cleanfiles(fileName, type, fileFolder):
    try:
        newName = re.sub( r'[^a-zA-Z0-9]', ' ', fileName) # thank you tinykat and alphabetagama
        newName = re.sub( r'[ ]+', ' ', newName)
        number = 1
        while os.path.isfile(fileFolder + newName + "." + type): # if the name already exist add a number to it
            newName = newName + "_" + str(number)
            number += 1
        newName = fileFolder + newName + "." + type
        oldName = fileFolder + fileName + "." + type
        os.rename(oldName, newName)
        print(oldName + " -----> " + newName)
    except:
       print("Failed in cleanfiles")


def getfiles(folder, type):
    try:
        for e in glob.glob(folder + "*." + type):
            cleanfiles(Path(e).stem, type, folder)
    except:
        print("Failed in getfiles")

def main(argv):
    fileFolder = ""
    fileType = ""
    try:
        opts, args = getopt.getopt(argv, "h:f:t:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("Error test.py -i <fileFolder> -o <fileType>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('test.py -i <fileFolder> -o <fileType>')
            sys.exit()
        elif opt in ("-f", "--ifile"):
            fileFolder = arg
        elif opt in ("-t", "--ofile"):
            fileType = arg
    print('fileFolder file is "' + fileFolder)
    print('fileType file is "' + fileType)
    getfiles(fileFolder, fileType)

if __name__ == "__main__":
   main(sys.argv[1:])