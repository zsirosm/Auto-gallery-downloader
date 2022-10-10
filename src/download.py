from gallery_dl import config

from downloader.gallery_dl_control import loadInitialConfig, buildUrl, processArtist



# load artists from file
def processWebsite(domainName, fileName = None):
    file = open(f"{fileName or domainName}.txt")
    urlFunc = buildUrl(domainName)
    with file:
        for artist in file:
            artist = artist.strip()
            processArtist(urlFunc, artist, {})



loadInitialConfig()

# processWebsite("twitter")
# processWebsite("deviantart")
processWebsite("kemono")

# ------- UPDATE MODE -----------------------------

# config.set(("extractor", "twitter"), "skip", "abort:20")
# processWebsite("twitter", "twitter-generated")

# config.set(("extractor", "deviantart"), "skip", "abort:2")
# processWebsite("deviantart", "deviantart-old")