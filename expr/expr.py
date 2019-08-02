from bs4 import BeautifulSoup
import requests
import re
import time
# url = 'https://myanimelist.net/topanime.php'

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# print(soup.prettify())

# logo = soup.find(id='logo-default')
# print(soup.title)
# print(soup.a)
# print(soup.find_all('table'))

# table = soup.table
# print(table)
# print(table['class'])
# print(soup.find(class_='top-ranking-table'))

# rankTab = soup.find(class_="top-ranking-table")
# items = rankTab.find_all("tr", class_="ranking-list")

# print(len(items))

# first = items[0]

# print(first.find(class_='detail').get_text())


def getRankingTable(startIdx):
    url = 'https://myanimelist.net/topanime.php?limit=%d' % startIdx
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find(class_="top-ranking-table")


def getDetail(item):
    return item.find(class_='detail')


def getTitle(item):
    return getDetail(item).find("a").get_text()


def getInfo(item):
    return getDetail(item).find(class_="information").get_text()


def getScore(item):
    return item.find(class_="js-top-ranking-score-col").getText()


def getAllData(item):
    title = getTitle(item)

    info = getInfo(item)
    infos = list(map(lambda s: s.strip(), re.split("\n", info)))
    kind = infos[1]
    date = infos[2]
    members = infos[3]

    score = getScore(item)

    return (title, kind, date, members, score)


def recordTable(startIdx, file):
    rankTab = getRankingTable(startIdx)
    items = rankTab.find_all("tr", class_="ranking-list")
    minScore = 10
    for item in items:
        allData = getAllData(item)
        score = float(allData[-1])
        if(score < minScore):
            minScore = score
        stringData = "\t".join(allData)
        dataFile.write(stringData+"\n")
    return minScore

# # rankTab = soup.find(class_="top-ranking-table")
# rankTab = getRankingTable(1)
# items = rankTab.find_all("tr", class_="ranking-list")


dataFile = open("data.tsv", "w")
startIdx = 0
score = 10
maxPages = 100
minScore = 7
while True:
    print('getting %d, score: %f' % (startIdx, score))
    score = recordTable(startIdx, dataFile)
    startIdx += 1
    if(score < minScore or startIdx >= maxPages):
        break
    else:
        time.sleep(5)


# recordTable(0, dataFile)
# time.sleep(2)
# recordTable(1, dataFile)
# time.sleep(2)
# recordTable(2, dataFile)
# for item in items:

#     # title = getTitle(item)

#     # info = getInfo(item)
#     # infos = list(map(lambda s: s.strip(), re.split("\n", info)))
#     # kind = infos[1]
#     # date = infos[2]
#     # members = infos[3]

#     # score = float(getScore(item))

#     allData = getAllData(item)
#     stringData = "\t".join(allData)
#     # print('%s : %s : %s : %s : %f' % allData)
#     print(stringData)
#     dataFile.write(stringData+"\n")

dataFile.close()
