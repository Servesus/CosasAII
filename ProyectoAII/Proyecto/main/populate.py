from bs4 import BeautifulSoup
import urllib.request
from main.models import Game, Tag, Offer, User
from datetime import datetime

def deleteGamesTables():
    Offer.objects.all().delete()
    Tag.objects.all().delete()
    Game.objects.all().delete()

def deleteUsers():
    User.objects.all().delete()


def populateTags():
    print("Loading tags...")
    tagList = []
    f = urllib.request.urlopen("https://store.steampowered.com/tag/browse/#global_492")
    s = BeautifulSoup(f,'html.parser')

    s2 = s.find("div", id = "tag_browse_global")
    tags = s2.find_all("div", class_ = "tag_browse_tag")

    for t in tags:
        tagId = t.get("data-tagid")
        name = t.get_text()

        tagList.append(Tag(idTag=tagId, name=name))

    Tag.objects.bulk_create(tagList)
    print("Tags inserted: " + str(Tag.objects.count()))
    print("---------------------------------------------------------")


def populateGames():
    print("Loading games...")
    f = urllib.request.urlopen("https://store.steampowered.com/games/#p=0&tab=ConcurrentUsers")
    s = BeautifulSoup(f,'html.parser')

    s2 = s.find_all("span", id = "ConcurrentUsers_links")
    s3 = s2.find_all("span", class_ = "paged_items_paging_pagelink")
    count = int(s3[5].get_text())

    for i in range(0, count):
        path = "https://store.steampowered.com/games/#p=" + str(i) + "&tab=ConcurrentUsers"
        f = urllib.request.urlopen(path)
        s = BeautifulSoup(f,'html.parser')

        s2 = s.find_all("div", id = "ConcurrentUsersRows")
        s3 = s2.find_all("a")
        for a in s3:
            tagList = []
            href = a.get("href")
            gameId = a.get("data-ds-appid")
            name = a.find("div", class_ = "tab_item_name").get_text()
            tagsId = a.get("data-ds-tagids").strip('][').split(',')
            for t in tagsId:
                tagList.append(Tag.objects.get(int(t)))

            g = Game(idGame=gameId, name=name, tags=tagList)
            g.save()

            price = a.find("div", class_ = "discount_final_price").get_text()
            if(price=="Free to Play"):
                p = 0.0
            else:
                price = price.strip("€").replace(",", ".")
                p = float(price)

            o = Offer(offerURL=href, price=p, site="Steam", game=g)
            o.save()


    print("Games inserted: " + str(Game.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateGamesDatabase():
    deleteGamesTables()
    populateTags()
    populateGames()
    print("Finished database population")
    
if __name__ == '__main__':
    populateGamesDatabase()