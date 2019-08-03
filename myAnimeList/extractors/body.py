def getName(soup):
    return soup.find('span', {'itemprop': 'name'}).text


def getSidePanelLabels(soup):
    return soup.find(id="content").find_all(class_="dark_text")


def getSidePanelItems(soup):
    sidePanelLabels = getSidePanelLabels(soup)
    return list(map(lambda label: label.parent, sidePanelLabels))


def getRelatedItems(soup):
    table = soup.find(class_='anime_detail_related_anime')
    if table == None:
        return []

    links = table.find_all('a')
    return list(map(lambda a: 'https://myanimelist.net'+a['href'], links))
