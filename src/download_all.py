from multiprocessing import Process

from downloader.downloader import launchDownloader, registerLogger

# ----- EXECUTION PART --------------------------------------

if __name__ == "__main__":

    print("Launching download...")

    Process(target = launchDownloader, args = ("deviantart",  ["update", "download"])).start()
    Process(target = launchDownloader, args = ("twitter", ["update", "download"])).start()
    Process(target = launchDownloader, args = ("kemonoparty", ["update", "download"])).start()


# print("Launching download...")
# loadInitialConfig()

# registerLogger("deviantart")
# registerLogger("twitter")
# # seem to be doing nothing atm
# registerLogger("gallery-dl")
# registerLogger("gallery-dl.downloader")
# registerLogger("gallery-dl.job")
# registerLogger("config")
# registerLogger("cache")
# registerLogger("unsupported")


# config.set(("extractor", "deviantart"), "skip", "abort:2")
# config.set(("extractor", "twitter"), "skip", "abort:20")

# deviantart = DownloaderThread(1, "deviantart", ["update"])
# twitter = DownloaderThread(2, "twitter", ["update"])

# deviantart.daemon = True
# twitter.daemon = True

# deviantart.start()
# twitter.start()

# active = True
# while active:
#     active = deviantart.is_alive() or twitter.is_alive()
#     time.sleep(3)


# Downloader("deviantart",  ["update"]).run()
# Downloader("twitter", ["update"]).run()

# Downloader("deviantart", ["download"]).run()
# Downloader("twitter", ["download"]).run()
# Downloader("kemonoparty", ["download"]).run()


# config.set(("extractor", "deviantart"), "skip", "abort:2")
# accountsDA = database.getAccountsToUpdate("deviantart")
# updateAccounts("deviantart", accountsDA)
# config.set(("extractor", "twitter"), "skip", "abort:20")
# accountsT = database.getAccountsToUpdate("twitter")
# updateAccounts("twitter", accountsT)


# config.clear()
# loadInitialConfig()
# newAccountsDA = database.getAccountsToDownload("deviantart")
# updateAccounts("deviantart", newAccountsDA)
# newAccountsT = database.getAccountsToDownload("twitter")
# updateAccounts("twitter", newAccountsT)

# accountsKemono = database.getAccountsToDownload("kemonoparty")
# updateAccounts("kemonoparty", accountsKemono)
