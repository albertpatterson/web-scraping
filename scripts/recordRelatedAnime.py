from bs4 import BeautifulSoup
import requests
import time
import datetime
import os

from common.AnimeDetails import AnimeDetails
from myAnimeList.extractors import body
from myAnimeList.extractors import sidePanel


def getStartDate(aired):
    if aired == 'NULL':
        return 'NULL'

    if len(aired) <= 11:
        start = aired
    elif aired[5] == ',':
        start = aired[:11]
    else:
        start = aired[:12]

    try:
        return str(datetime.datetime.strptime(start, '%b %d, %Y'))
    except:
        return aired


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
        name = body.getName(soup)
    except:
        failed.append(url)
        return

    sidePanelItems = body.getSidePanelItems(soup)

    mediaType = sidePanel.getType(sidePanelItems)
    episodes = sidePanel.getEpisodes(sidePanelItems)
    aired = sidePanel.getAired(sidePanelItems)
    startDate = getStartDate(aired)
    studios = sidePanel.getStudios(sidePanelItems)
    genres = sidePanel.getGenres(sidePanelItems)
    rating = sidePanel.getRating(sidePanelItems)
    score = sidePanel.getScore(sidePanelItems)
    members = sidePanel.getMembers(sidePanelItems)

    animeDetails = AnimeDetails(
        name,
        mediaType,
        episodes,
        startDate,
        studios,
        genres,
        rating,
        score,
        members,
        url,
    )
    success.append(animeDetails)
    visited.add(url)

    relatedItems = body.getRelatedItems(soup)

    print(relatedItems)

    try:
        visitRelated = int(members.replace(',', '')) > 5e3
    except:
        visitRelated = True

    if visitRelated:
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


def recordRelatedAnime(name, startUrl):

    outputDir = 'out/relatedAnime'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    successfileAllName = '%s/%s_success_all.tsv' % (outputDir, name)
    successfileAnimatedName = '%s/%s_success_animated.tsv' % (outputDir, name)
    failfileName = '%s/%s_fail.tsv' % (outputDir, name)

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


titlesFile = open('data/AnimeTitles.tsv', 'r')

try:
    for line in titlesFile:
        parts = line.split('\t')
        name = parts[0]
        startUrl = parts[1]
        recordRelatedAnime(name, startUrl)
finally:
    titlesFile.close()
