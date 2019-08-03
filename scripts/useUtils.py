from bs4 import BeautifulSoup
import requests
from myAnimeList.extractors import body
from myAnimeList.extractors import sidePanel

url = 'https://myanimelist.net/anime/6811/InuYasha__Kanketsu-hen'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
sidePanelItems = body.getSidePanelItems(soup)

print("name", body.getName(soup))
print("English", sidePanel.getEnglish(sidePanelItems))
print("Type", sidePanel.getType(sidePanelItems))
print("Episodes", sidePanel.getEpisodes(sidePanelItems))
print("Aired", sidePanel.getAired(sidePanelItems))
print("Studios", sidePanel.getStudios(sidePanelItems))
print("Genres", sidePanel.getGenres(sidePanelItems))
print("getRating", sidePanel.getRating(sidePanelItems))
print("Score", sidePanel.getScore(sidePanelItems))
print("Members", sidePanel.getMembers(sidePanelItems))
