import os
import datetime
import hashlib


def getHash(file):
    sha256_hash = hashlib.sha256()
    with open(file,"rb") as f:
    # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()

def getDateCreatedTimestamp(file):
    time = os.path.getctime(file)
    return int(time)


# make hashes of files and store for later
files = os.scandir('temp')
hash_dict = {}

for file in files:
    path = os.path.realpath(file)
    time = getDateCreatedTimestamp(file)
    hash = getHash(file)
    
    print("dir: ", path)
    print("hash:", hash)

    list = hash_dict.get(hash, [])
    list.append({"file": file })
    hash_dict[hash] = list


# find and delete duplicates
print("hash dict", hash_dict)
for list in hash_dict.items():
    print("list length: ", len(list), list)
    if len(list) > 1:
        