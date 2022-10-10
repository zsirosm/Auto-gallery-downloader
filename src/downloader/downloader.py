import time
import logging

from gallery_dl import config, output

from downloader.database import database, getCurrentTime
# updateAccount, getAccountsToUpdate, getAccountsToDownload

from downloader.gallery_dl_control import loadInitialConfig, buildUrl, processArtist

def updateAccounts(accountType, accounts):
    updateTime = getCurrentTime()
    accountList = list(accounts)
    accountsToUpdate = len(accountList)
    print(f"Found {accountsToUpdate} accounts to update on {accountType}.")
    urlFunc = buildUrl(accountType)

    for index, account in enumerate(accountList):
        database.updateAccount(account.get("id"), {"updated": 0})
        processArtist(urlFunc, account.get("accountId"), account)
        database.updateAccount(account.get("id"), {"updated": updateTime})
        print(f"{index + 1} of {accountsToUpdate} {accountType} account processed, sleeping for 4 seconds.")
        time.sleep(4)


class CustomHandler(logging.Handler):
    def emit(self, logRecord):
        print("LOG EVENT: ", logRecord)

def registerLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    handler = CustomHandler()
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)


extractorSettings = {
    "deviantart": {
        "skip": "abort:2"
    },
    "twitter": {
        "skip": "abort:20"
    }
}

timeouts = {
    "deviantart": 36,
    "twitter": 8,
    "kemonoparty": 84,
}

class Downloader():
    def __init__(self, name, modes):
        self.name = name
        self.extractorSettings = extractorSettings.get(name, {})
        self.modes = modes
    
    def run(self):
        print(f"Starting thread {self.name}")

        for mode in self.modes:
            print("Starting work:", self.name, mode)
            modeFunc = self.getMode(mode)
            modeFunc()

    def getMode(self, mode):
        modeFunctions = {
            "update": self.update,
            "download": self.download,
        }

        def default(self):
            print(f"No action found for mode '{mode}'.")

        return modeFunctions.get(mode, default)

    def update(self):
        config.clear()
        loadInitialConfig()

        for option, value in self.extractorSettings.items():
            config.set(("extractor", self.name), option, value)

        hours = timeouts.get(self.name, 12)
        accounts = database.getAccountsToUpdate(self.name, hours * 3600000)


        updateAccounts(self.name, accounts)

    def download(self):
        config.clear()
        loadInitialConfig()

        accounts = database.getAccountsToDownload(self.name)
        updateAccounts(self.name, accounts)


def launchDownloader(name, modes):
    Downloader(name, modes).run()


