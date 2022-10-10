import sys

from downloader.database import database


def prepareAccountData(accountType, account):
    print("Account: ", account)
    if (accountType == "kemonoparty"):
        simplified = account.strip().rstrip()
        stringPieces = simplified.split("/")

        if (len(stringPieces) < 3):
            return { "name": "" }

        name = stringPieces[2]
        domain = stringPieces[0]
        return { "name": name, "extraData": { "extraPath": { "domain": domain }}}
    
    return { "name": account }


if (len(sys.argv) < 3):
    print("Error: This script requires two arguments")
    sys.exit()

knownTypes = ["deviantart", "twitter", "kemonoparty"]

accountType = sys.argv[1]
textfile = sys.argv[2]

if (not accountType in knownTypes):
    print(f"Error: Unknown type {accountType}")
    sys.exit()

file = open(textfile)

with file:
    added = 0
    existing = 0
    failed = 0
    total = 0
    for account in file:
        accountData = prepareAccountData(accountType, account)
        accountName = accountData.get("name").strip().rstrip()
        extraData = accountData.get("extraData", {})
        if accountName != "":
            response = database.insertNewAccount(accountType, accountName, extraData)
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