def getSidePanelValue(sidePanelItems, soughtLabel):
    for item in sidePanelItems:
        fullText = item.text.strip()
        if fullText.startswith(soughtLabel):
            return fullText[len(soughtLabel):].strip()
    return 'Null'


def getEnglish(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'English:')


def getType(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Type:')


def getEpisodes(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Episodes:')


def getAired(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Aired:')


def getStudios(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Studios:')


def getGenres(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Genres:')


def getRating(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Rating:')


def getScore(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Score:')[:4]


def getMembers(sidePanelItems):
    return getSidePanelValue(sidePanelItems, 'Members:')
