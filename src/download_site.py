import sys

from downloader.downloader import launchDownloader


knownTypes = ["deviantart", "twitter", "kemonoparty"]

if (len(sys.argv) < 2):
    print("Error: This script requires an argument: accountType")
    sys.exit()

accountType = sys.argv[1]

if (not accountType in knownTypes):
    print(f"Error: Unknown type {accountType}")
    sys.exit()


if __name__ == "__main__":

    print("Launching download...")

    launchDownloader(accountType,  ["update", "download"])