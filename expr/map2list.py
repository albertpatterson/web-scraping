from bs4 import BeautifulSoup
import requests
import time
import datetime

# name = 'Monogatari_Series'
# startUrl = 'https://myanimelist.net/anime/17074/Monogatari_Series__Second_Season'

# name = 'Suzumiya_Haruhi'
# startUrl = 'https://myanimelist.net/anime/7311/Suzumiya_Haruhi_no_Shoushitsu'

# name = 'Sora_no_Otoshimono'
# startUrl = 'https://myanimelist.net/anime/5958/Sora_no_Otoshimono'

# name = 'clannad'
# startUrl = 'https://myanimelist.net/anime/4181/Clannad__After_Story'

# name = 'Kara_no_Kyoukai'
# startUrl = 'https://myanimelist.net/anime/5205/Kara_no_Kyoukai_7__Satsujin_Kousatsu_Kou'

# name = 'Toradora'
# startUrl = 'https://myanimelist.net/anime/4224/Toradora'

# name = 'Kaichou_wa_Maid-sama!'
# startUrl = 'https://myanimelist.net/anime/7054/Kaichou_wa_Maid-sama'

# name = 'Shokugeki_no_Souma'
# startUrl = 'https://myanimelist.net/anime/32282/Shokugeki_no_Souma__Ni_no_Sara'

# name = 'Date_A_Live'
# startUrl = 'https://myanimelist.net/anime/15583/Date_A_Live?q=date%20a%20li'

# name = 'High_School_DxD'
# startUrl = 'https://myanimelist.net/anime/15451/High_School_DxD_New'

# name = 'To_LOVE-Ru'
# startUrl = 'https://myanimelist.net/anime/31711/To_LOVE-Ru_Darkness_2nd_Specials'

# name = 'God_Eater'
# startUrl = 'https://myanimelist.net/anime/27631/God_Eater'

# name = 'Shingeki_no_Kyojin'
# startUrl = 'https://myanimelist.net/anime/38524/Shingeki_no_Kyojin_Season_3_Part_2'

# name = ''
# startUrl = ''

# successfileAllName = 'related/%s_success_all.tsv' % name
# successfileAnimatedName = 'related/%s_success_animated.tsv' % name
# failfileName = 'related/%s_fail.tsv' % name


class AnimeDetails:

    header = "\t".join(
        ['name', 'media type', 'episode count', 'dates aired', 'rating', 'url'])

    def __init__(self, name, mediaType, episodeCount, startDate, rating, url):
        self.name = name
        self.mediaType = mediaType
        self.episodeCount = episodeCount
        self.startDate = str(startDate)
        self.rating = rating
        self.url = url

    def __str__(self):
        return '\t'.join([self.name, self.mediaType, self.episodeCount, self.startDate, self.rating, self.url])


# success = []
# failed = []
# visited = set()


# def reset():
#     success.clear()
#     failed.clear()
#     visited.clear()


def getName(soup):
    name = soup.find('span', {'itemprop': 'name'}).text
    return name


def getSidePanelLabels(soup):
    return soup.find(id="content").find_all(class_="dark_text")


def getSidePanelValue(soup, test, extractValue):
    sidePanelLabels = getSidePanelLabels(soup)

    for label in sidePanelLabels:
        if test(label):
            return extractValue(label)

    return 'NULL'


def getSidePanelElementValue(soup, soughtLabel):
    def test(label): return label.text == soughtLabel
    def extractValue(label): return label.findNext().text

    return getSidePanelValue(soup, test, extractValue)


def getSidePanelTextValue(soup, soughtLabel):
    def test(label): return label.text == soughtLabel

    def extractValue(label):
        return label.parent.text.strip()[len(soughtLabel):].strip()

    return getSidePanelValue(soup, test, extractValue)


def getMediaType(soup):
    return getSidePanelElementValue(soup, 'Type:')


def getEpisodeCount(soup):
    return getSidePanelTextValue(soup, 'Episodes:')


def getStartDate(soup):
    aired = getSidePanelTextValue(soup, 'Aired:')

    if aired == 'NULL':
        return 'NULL'

    if len(aired) <= 11:
        start = aired
    elif aired[5] == ',':
        start = aired[:11]
    else:
        start = aired[:12]

    print(start)
    try:
        return datetime.datetime.strptime(start, '%b %d, %Y')
    except:
        return aired


def getRating(soup):
    return getSidePanelElementValue(soup, 'Score:')


def getRelatedItems(soup):
    table = soup.find(class_='anime_detail_related_anime')
    if table == None:
        return []

    links = table.find_all('a')
    return list(map(lambda a: 'https://myanimelist.net'+a['href'], links))

# recordedMediaTypes = ['TV', 'ONA', 'OVA', '']


def visitPage(urlRaw, success, failed, visited):
    url = urlRaw.strip()
    if(url in visited):
        print('skipping '+url)
        return

    print('visiting '+url)
    time.sleep(5)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        name = getName(soup)
    except:
        failed.append(url)
        return

    mediaType = getMediaType(soup)
    episodeCount = getEpisodeCount(soup)
    startDate = getStartDate(soup)
    rating = getRating(soup)
    relatedItems = getRelatedItems(soup)

    animeDetails = AnimeDetails(
        name, mediaType, episodeCount, startDate, rating, url)
    success.append(animeDetails)
    visited.add(url)

    print(relatedItems)
    for relatedItem in relatedItems:
        visitPage(relatedItem, success, failed, visited)


def writeData(success, failed, successFileAll, successFileAnimated, failFile):
    successFileAll.write(AnimeDetails.header)
    successFileAll.write('\n')

    successFileAnimated.write(AnimeDetails.header)
    successFileAnimated.write('\n')

    animatedTypes = ['TV', 'ONA', 'OVA', 'Movie', 'Special']

    success.sort(key=lambda d: d.startDate)

    for animeDetails in success:
        print(animeDetails)
        successFileAll.write(str(animeDetails))
        successFileAll.write('\n')

        if(animeDetails.mediaType in animatedTypes):
            successFileAnimated.write(str(animeDetails))
            successFileAnimated.write('\n')

    for failure in failed:
        failFile.write(failure)
        failFile.write('\n')


def recordMap(name, startUrl):
    successfileAllName = '../related/%s_success_all.tsv' % name
    successfileAnimatedName = '../related/%s_success_animated.tsv' % name
    failfileName = '../related/%s_fail.tsv' % name

    success = []
    failed = []
    visited = set()

    visitPage(startUrl, success, failed, visited)

    successFileAll = open(successfileAllName, "w")
    successFileAnimated = open(successfileAnimatedName, "w")
    failFile = open(failfileName, "w")

    try:
        writeData(success, failed, successFileAll,
                  successFileAnimated, failFile)
    finally:
        successFileAll.close()
        successFileAnimated.close()
        failFile.close()


titlesFile = open('AnimeTitles.tsv', 'r')

try:
    for line in titlesFile:
        parts = line.split('\t')
        name = parts[0]
        startUrl = parts[1]
        recordMap(name, startUrl)
finally:
    titlesFile.close()

# name = 'Kimi_no_Na_wa'
# startUrl = 'https://myanimelist.net/anime/32281/Kimi_no_Na_wa'

# recordMap(name, startUrl)

# successFileAll = open(successfileAllName, "w")
# successFileAll.write(AnimeDetails.header)
# successFileAll.write('\n')

# successFileAnimated = open(successfileAnimatedName, "w")
# successFileAnimated.write(AnimeDetails.header)
# successFileAnimated.write('\n')

# animatedTypes = ['TV', 'ONA', 'OVA', 'Movie', 'Special']

# success.sort(key=lambda d: d.startDate)

# for animeDetails in success:
#     print(animeDetails)
#     successFileAll.write(str(animeDetails))
#     successFileAll.write('\n')

#     if(animeDetails.mediaType in animatedTypes):
#         successFileAnimated.write(str(animeDetails))
#         successFileAnimated.write('\n')


# successFileAll.close()
# successFileAnimated.close()

# failFile = open(failfileName, "w")
# for failure in failed:
#     failFile.write(failure)
#     failFile.write('\n')

# failFile.close()
