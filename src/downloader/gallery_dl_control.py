from gallery_dl.job import DownloadJob
from gallery_dl import config



# Initial set config and directory, taken from manual Gallery-dl location
def loadInitialConfig():
    config.set((), "base-directory", "Z:\gallery-dl\gallery-dl")
    configFile = ("F:\Downloads\Gallery-dl\gallery-dl.conf",)
    config.load(configFile, True)


# define URL builder function for domain, then register it in the dictionary
def buildUrl(domain):
    def builderTwitter(artistId, artist):
        return f"https://twitter.com/{artistId}/media"

    def builderDeviantart(artistId, artist): 
        return f"https://www.deviantart.com/{artistId}"

    #old downloader for simple download from file
    def builderKemono(artistId, artist):
        return f"https://kemono.party/{artistId}"

    def builderKemonoparty(artistId, artist):
        extraPath = artist.get("extraPath")
        domain = extraPath.get("domain")
        return f"https://kemono.party/{domain}/user/{artistId}"

    # dictionary
    domains = {
        "twitter": builderTwitter,
        "deviantart": builderDeviantart,
        "kemono": builderKemono,
        "kemonoparty": builderKemonoparty,
    }
    return domains.get(domain, "")


def processArtist(urlFunc, artistName, artist):
    if artistName == "":
        return
        
    url = urlFunc(artistName, artist)
    accountType = artist.get("type", "")
    print(f"Processing artist {accountType} {artistName}:")
    print("URL:", url)
    DownloadJob(url).run()





# ------------ TESTS ---------------------
# config.set(("extractor", "twitter"), "sleep", 10)

# link = "https://kemono.party/patreon/user/9961216"
# x = DownloadJob(link)
# x.run()