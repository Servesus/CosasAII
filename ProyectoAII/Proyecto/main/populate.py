from bs4 import BeautifulSoup
import urllib.request
import math
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

    s2 = s.find("span", id = "ConcurrentUsers_end")
    s3 = s.find("span", id = "ConcurrentUsers_total")
    itemsShowed = int(s2.get_text())
    total = s3.get_text().split(",")
    total = int(total[0]+total[1])
    count = math.ceil(total/itemsShowed)

    for i in range(0, count-1):
        path = "https://store.steampowered.com/games/#p=" + str(i) + "&tab=ConcurrentUsers"
        f = urllib.request.urlopen(path)
        s = BeautifulSoup(f,'html.parser')

        s2 = s.find("div", id = "ConcurrentUsersRows")
        s3 = s2.find_all("a")
        for a in s3:
            tagList = []
            href = a.get("href")
            gameId = a.get("data-ds-appid")
            name = a.find("div", class_ = "tab_item_name").get_text()
            tagsId = a.get("data-ds-tagids").strip('][').split(',')

            g = Game(idGame=gameId, name=name)
            g.save()
            #g.tags.set(tagList)
            for t in tagsId:
                tId = int(t)
                tag = Tag.objects.get(pk=tId)
                g.tags.add(tag)
                g.save()
                #tagList.append(tag)

            tags = g.tags

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