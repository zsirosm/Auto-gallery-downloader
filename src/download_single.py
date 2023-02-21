import sys

from downloader.database import database
from downloader.downloader import updateAccounts
from downloader.gallery_dl_control import loadInitialConfig

knownTypes = ["deviantart", "twitter", "kemonoparty"]

if (len(sys.argv) < 3):
    print("Error: This script requires two arguments")
    sys.exit()

accountName = sys.argv[1]
accountType = sys.argv[2]

if (not accountType in knownTypes):
    print(f"Error: Unknown type {accountType}")
    sys.exit()

account = database.checkForAccount(accountType, accountName)

print("account", account)

loadInitialConfig()
updateAccounts(accountType, account)