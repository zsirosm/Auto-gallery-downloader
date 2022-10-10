import os

print('Hello World!')
config = "something"

def printFunction(c = config):
    print(c)

printFunction()

# dir = Path('F:\\')
# fileList = dir.iterdir()
# for file in fileList:
#     printFunction(file)

textfile = open("test.txt", "w")

with open("test.txt", "w") as outputFile:
    files = os.scandir('F:\Downloads\Gallery-dl\gallery-dl\deviantart')
    for file in files:
        outputFile.write(f"{file.name}\n")