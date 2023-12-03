import time
from gallery_dl.job import DownloadJob
from gallery_dl import config

from downloader.database import database, getCurrentTime


# Initial set config and directory, taken from manual Gallery-dl location
def loadInitialConfig():
    config.set((), "base-directory", "Z:\gallery-dl\gallery-dl")
    configFile = ("gallery-dl\gallery-dl.conf",)
    config.load(configFile, True)


# define URL builder function for every website, then register it in the dictionary
def buildUrl(website):
    def builderTwitter(account):
        artistId = account.get("accountId")
        return f"https://twitter.com/{artistId}"

    def builderDeviantart(account): 
        artistId = account.get("accountId")
        return f"https://www.deviantart.com/{artistId}"

    def builderKemonoparty(account):
        artistId = account.get("accountId")
        extraPath = account.get("extraPath")
        domain = extraPath.get("domain")
        return f"https://kemono.party/{domain}/user/{artistId}"

    # dictionary
    domains = {
        "twitter": builderTwitter,
        "deviantart": builderDeviantart,
        "kemonoparty": builderKemonoparty,
    }
    return domains.get(website, "")

# processes single account
def processAccount(account):

    accountName = account.get("accountId")
    accountType = account.get("type", "")

    print(f"Processing artist {accountType} {accountName}:")

    url = buildUrl(accountType)(account)
    print("URL:", url)
    DownloadJob(url).run()

# processes list of accounts, requires list of accounts from the database
def processAccounts(accountType, accounts):
    updateTime = getCurrentTime()
    accountList = list(accounts)
    accountsToUpdate = len(accountList)
    print(f"Found {accountsToUpdate} accounts to update on {accountType}.")

    for index, account in enumerate(accountList):
        accountId = account.get("id")
        database.updateAccount(accountId, {"updated": 0})
        processAccount(account)
        database.updateAccount(accountId, {"updated": updateTime})
        print(f"{index + 1} of {accountsToUpdate} {accountType} account processed, sleeping for 3 seconds.")
        time.sleep(3)




# should be moved to separate file
# used just for update mode for now, should be expanded
extractorSettings = {
    "deviantart": {
        "skip": "abort:2"
    },
    "twitter": {
        "skip": "abort:20"
    }
}

# prevent too frequent updates of the same accounts
timeouts = {
    "deviantart": 36,
    "twitter": 36,
    "kemonoparty": 168,
}

# main class, supply website and modes
class Downloader():
    def __init__(self, domain, modes):
        self.name = domain
        self.extractorSettings = extractorSettings.get(domain, {})
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

    # -------------------modes-----------------------------------------

    # only updates accounts, applies "extractorSettings" to skip downloading everything and only updates accounts older than "timeout"
    def update(self):
        config.clear()
        loadInitialConfig()

        for option, value in self.extractorSettings.items():
            config.set(("extractor", self.name), option, value)

        hours = timeouts.get(self.name, 12)
        accounts = database.getAccountsToUpdate(self.name, hours * 3600000)

        processAccounts(self.name, accounts)


    # download everything
    def download(self):
        config.clear()
        loadInitialConfig()

        accounts = database.getAccountsToDownload(self.name)

        processAccounts(self.name, accounts)


def launchDownloader(name, modes):
    Downloader(name, modes).run()


