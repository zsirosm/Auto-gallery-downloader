import sys

from downloader.database import database


def prepareAccountData(accountRow, fieldNames):
    rawAccount = {}
    pieces = accountRow.split(" - ")
    for index, property in enumerate(pieces):
        fieldName = fieldNames[index]
        rawAccount[fieldName]= property.strip().rstrip()

    if (rawAccount["type"] == "kemonoparty"):        
        extraPath = {"domain": rawAccount["extraPath.domain"]}
        rawAccount["extraPath"] = extraPath

    rawAccount["updated"] = int(rawAccount["updated"])
    rawAccount["created"] = int(rawAccount["created"])

    rawAccount['id'] = rawAccount['uuid']

    del rawAccount["extraPath.domain"]
    del rawAccount['uuid']
    
    return rawAccount




if (len(sys.argv) < 2):
    print("Error: This script requires one argument")
    sys.exit()

knownTypes = ["deviantart", "twitter", "kemonoparty"]

textfile = sys.argv[1]

file = open(textfile)

with file:
    added = 0
    existing = 0
    failed = 0
    total = 0
    fields = None
    for index, accountRow in enumerate(file):
        if (index == 0):
            pieces = accountRow.split("-")
            fields = []
            for property in pieces:
                fields.append(property.strip().rstrip())

            print("Fields: ", fields)

            continue

        if accountRow != "":
            accountData = prepareAccountData(accountRow, fields)
            response = database.insertNewAccount(accountData.pop("type"), accountData.pop("accountId"), accountData)
            status = response.get("status")
            if ( status == "success"):
                added += 1
            elif (status == "info"):
                existing += 1
            else:
                print("Error message:", response["message"])
                failed += 1

            total += 1

        else:
            print("Empty ")

    print(f"Added {added} accounts\nAlready existing {existing} accounts\nFailed {failed} accounts\nTotal: {total}")