import sys

from downloader.database import database
from downloader.downloader import processAccounts, loadInitialConfig

knownTypes = ["deviantart", "twitter", "kemonoparty"]

if (len(sys.argv) < 3):
    print("Error: This script requires two arguments: accountType, accountName")
    sys.exit()

accountType = sys.argv[1]
accountName = sys.argv[2]

if (not accountType in knownTypes):
    print(f"Error: Unknown type {accountType}")
    sys.exit()

account = database.checkForAccount(accountType, accountName)

print("account", account)

loadInitialConfig()
processAccounts(accountType, account)