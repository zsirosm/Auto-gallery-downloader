import os, sys
import hashlib
import json
import copy


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

def deleteDuplicates(folder):

    # make hashes of files and store for later
    files = os.scandir(folder)
    hash_dict = {}

    index = 0
    for file in files:
        index += 1
        path = os.path.realpath(file)
        time = getDateCreatedTimestamp(file)
        hash = getHash(file)
        print("index: ", index)
        print("dir: ", path)

        date = file.name[0:11]
        hash = date + hash
        print("hash:", hash)

        list = hash_dict.get(hash, [])
        list.append({"filename": file.name, "created_time": time, "path": path })
        hash_dict[hash] = list


    report = {"all_files": copy.deepcopy(hash_dict)}

    # find and delete duplicates


    files_to_keep = []
    skipped_files = {}
    for hash, file_list in hash_dict.items():
        # check duplicates of each hash
        print("list length: ", len(file_list), "; list hash: ", hash)

        if (len(file_list) <= 1):
            skipped_files[hash] = file_list
            continue

        # find the newest file, it will be removed from the hash list and kept
        index_of_newest = 0
        created_time = file_list[0].get("created_time")
        for list_index, file in enumerate(file_list):
            if (file.get("created_time") > created_time):
                index_of_newest = list_index
                created_time = file.get("created_time")
        
        keep_this = file_list.pop(index_of_newest)
        files_to_keep.append(keep_this)

        # remove the rest of duplicates
        for file in file_list:
            try:
                os.remove(file.get("path"))

            except OSError as e:
                # If it fails, inform the user.
                print("FILE REMOVAL Error: %s - %s." % (e.filename, e.strerror))

    report["_number_of_hashes"] = len(hash_dict)
    report["_number_of_kept_files"] = len(files_to_keep)
    report["_number_of_skipped_files"] = len(skipped_files)
    report["files_to_keep"] = files_to_keep
    report["skipped_files"] = skipped_files


    report_filename = 'report_files\\' + 'report--' + folder.replace('\\', '-').replace(':', '-') + '.json'

    with open(report_filename, 'w') as jsonfile:
        json.dump(report, jsonfile)


#-----------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    folder = sys.argv[1]
    deleteDuplicates(folder)