import os, sys
import time
from delete_dupes import deleteDuplicates

mainFolder = sys.argv[1]

files = os.scandir(mainFolder)

for file in files:
    print("folder:", file.name)
    folder = mainFolder + '\\' + file.name

    deleteDuplicates(folder)

    print("Folder ", file.name, " processed!")
    time.sleep(3)