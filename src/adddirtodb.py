import os
import sys

from downloader.database import database

if (len(sys.argv) < 2):
    print("Error: This script requires an argument")
    sys.exit()


accountType = sys.argv[1]

files = os.scandir(f'F:\Downloads\Gallery-dl\gallery-dl\\{accountType}')
added = 0
existing = 0
failed = 0
total = 0
for file in files:
    accountName = file.name.strip().rstrip()
    response = database.insertNewAccount(accountType, accountName)
    status = response.get("status")
    if ( status == "success"):
        added += 1
    elif (status == "info"):
        existing += 1
    else:
        failed += 1

    total += 1

print(f"Added {added} accounts\nAlready existing {existing} accounts\nFailed {failed} accounts\nTotal: {total}")