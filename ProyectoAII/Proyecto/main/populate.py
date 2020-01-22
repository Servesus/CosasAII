from main.models import User, Game, Tag
from datetime import datetime
import csv

path = "steam"

def deleteTables():  
    User.objects.all().delete()
    Tag.objects.all().delete()
    Game.objects.all().delete()

    
def populateGames():
    print("Loading games...")
        
    with open(path+"\\steam.csv", encoding="utf8") as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        #count = len(csv_reader) + 1
        count = 500
        for i in range(1, count):
            row = csv_reader[i]
            tags = []
            g = Game(idGame=row[0], name=row[1])
            g.save()
            g.tags.clear()
            tagNames = row[10].split(';')
            for t in tagNames:
                tag, _ = Tag.objects.get_or_create(name=t)
                tags.append(tag)

            g.tags.set(tags)
            g.save()
            print("Added game " + str(i) + "/" + str(count))
    
    print("Games inserted: " + str(Game.objects.count()))
    print("Tags inserted: " + str(Tag.objects.count()))
    print("---------------------------------------------------------")
    
def populateDatabase():
    deleteTables()
    populateGames()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()