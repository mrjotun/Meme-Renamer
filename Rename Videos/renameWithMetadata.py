import sys, getopt, os
import subprocess
import glob

def renameFileWithMetadata(file, type, fileFolder):
    try:
        exe = "exiftool.exe"
        input_file = file
        process = subprocess.Popen([exe, input_file], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, universal_newlines=True)
        info = {}
        for output in process.stdout:
            line = output.strip().split(":")
            info[line[0].strip()] = line[1].strip()

        if "Title" in info:
            if info["Title"] != "":
                newName = fileFolder + info["Title"] + "." + type
                number = 1
                newName = newName.replace("..",".") #sometimes the metaname contains a . at the end. leading to => something..avi
                if file != newName:
                    while os.path.isfile(newName): # if the name already exist add a number to it
                        newName = fileFolder + info["Title"] + "_" + str(number) + "." + type
                        number += 1
                    os.rename(file,newName)
                    print(file + " ---> " + newName)
                else:
                    print(file + " has the same name in the meta")
        else:
            print(file + " missing title tag")
    except:
        print("Rename failed on this file: " + file)


def getfiles(folder, type):
    try:
        for e in glob.glob(folder+ "*." + type):
            renameFileWithMetadata(e.replace("\\","/"), type, folder) # glob adds \\ before the filename. 
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