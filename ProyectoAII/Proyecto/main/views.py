import shelve
from main.models import User, Game, Tag
from main.forms import GameForm, TagForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.populate import populateDatabase
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup,NavigableString

"""
# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.film.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()
"""   


    
#  CONJUNTO DE VISTAS

def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

"""
def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')
"""

"""
# APARTADO A
def recommendedFilmsUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            films = []
            scores = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})

# APARTADO B
def recommendedFilmsItems(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:2]
            films = []
            scores = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})

# APARTADO C
def similarFilms(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            films = []
            similar = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                similar.append(re[0])
            items= zip(films,similar)
            return render(request,'similarFilms.html', {'film': film,'films': items})
    form = FilmForm()
    return render(request,'search_film.html', {'form': form})

# APARTADO D
def recommendedUsersFilms(request):
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['ItemsPrefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idFilm))
            recommended = rankings[:3]
            films = []
            scores = []
            for re in recommended:
                films.append(UserInformation.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'recommendationUsers.html', {'film': film, 'items': items})
    form = FilmForm()
    return render(request,'search_film.html', {'form': form})
"""

def search(request):
    if request.method=='GET':
        form = GameForm(request.GET, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            nombres,links,imagenes,precios,s = offers(name)
            """
            return render(request, 'offers.html', 
                {'nombres': nombres, 'links': links, 'imagenes': imagenes, 'precios': precios, 'site': s, 'range': range(len(s))})
            """
            lst = [{'item1': t[0], 'item2': t[1], 'item3':t[2], 'item4': t[3], 'item5': t[4]} for t in zip(nombres,links,imagenes,precios,s)]
            return render(request, 'offers.html', {'lst': lst})
        else:
            form=GameForm()
            return render(request,'search_game.html', {'form':form })


def offers(name):
    nombres,links,imagenes,precios,s = [],[],[],[],[]
    try:
        instantgaming(name, nombres, links, imagenes, precios, s)
    except:
        pass
    try:
        eneba(name, nombres, links, imagenes, precios, s)
    except:
        pass
    try:
        g2a(name, nombres, links, imagenes, precios, s)
    except:
        pass
    
    #gamersgate(name, nombres, links, imagenes, precios, s)
    

    return nombres,links,imagenes,precios,s


def searchTag(request):
    if request.method=='GET':
        form = TagForm(request.GET, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            tag = Tag.objects.get(name=name)
            games = Game.objects.filter(tags__contains=tag)
            if len(games) == 0:
                form=UserForm()
                return render(request,'search_tag.html', {'form':form })
            else:
                return render(request,'games.html', {'games':games })

        else:
            form=UserForm()
            return render(request,'search_tag.html', {'form':form })

def instantgaming(juego, nombres, links, imagenes, precios, s):
    site = "https://www.instant-gaming.com/en/search/?q="+str(juego.replace(' ', '%20'))
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    juegos = soup.find("div",class_="search")
    for juego in juegos:
        try:
            if isinstance(juego, NavigableString):
                continue
            nombre = juego.find("div",class_="name").string
            a = juego.find("a")
            link = a.get("href")
            precio = a.find("div", class_="price").string.strip('\n').strip('€')
            try:
                p = float(precio)
            except:
                p = 'N/A'
            imagen = a.find("img").get("src")

            nombres.append(nombre)
            links.append(link)
            precios.append(p)
            imagenes.append(imagen)
            s.append("Instant Gaming")
        except:
            pass

def g2a(busqueda, nombres, links, imagenes, precios, s):
    site = "https://www.g2a.com/search?query="+str(busqueda.replace(' ', '%20'))
    hdr = {"authority": "www.g2a.com",
            "method": "GET",
            "path": "/search?query=gta",
            "scheme": "https",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "referer": "https://www.g2a.com",
            "sec-fetch-mode": "navigate",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,'html.parser')
    juegos = soup.find("ul",class_="products-grid")
    for juego in juegos:
        try:
            card_media = juego.find("div",class_="Card__media")
            link = "https://www.g2a.com" + card_media.a.get("href")
            try:
                req2 = Request(link, headers=hdr)
                page2 = urlopen(req2)
                soup2 = BeautifulSoup(page2, 'html.parser')
                imagen = soup2.find('img', class_="lazy-image__img").get('data-src')
            except:
                imagen = ""
            nombre = juego.find("h3",class_="Card__title").a.string
            tags_precio = juego.find("div",class_="Card__body").find("div",class_="Card__footer").find("div",class_="Card__price").find("span",class_="Card__price-cost price")
            precio = str(tags_precio).split(">")[1].split("<")[0]
            
            nombres.append(nombre)
            links.append(link)
            precios.append(float(precio))
            imagenes.append(imagen)
            s.append("G2A")
        except:
            pass

def eneba(busqueda, nombres, links, imagenes, precios, s):
    site = "https://www.eneba.com/search?page=1&text="+busqueda+"&types[]=game"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    s2 = soup.find("div",class_="_1tD0CW").section.div
    juegos = s2.contents[1].contents
    for juego in juegos:
        try:
            imagen = juego.find("div",class_="_2vZ2Ja _1p1I8b").find("img").get("src")
            nombre = juego.find("div",class_="_2vZ2Ja _1p1I8b").find("img").get("alt")
            link = "https://www.eneba.com" + str(juego.find("div",class_="_12ISZC").a.get("href"))
            p = str(juego.find("div",class_="d6Cxnh").find_all("span",class_="_3RZkEb"))
            p2 = p.split('€')
            p3 = p2[1].split('<')
            precio = p3[0]

            nombres.append(nombre)
            links.append(link)
            precios.append(float(precio))
            imagenes.append(imagen)
            s.append("Eneba")
        except:
            pass


def gamersgate(juego, nombres, links, imagenes, precios, s):
    site = "https://es.gamersgate.com/games?prio=relevance&q=%22+" + juego
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    juegos = soup.find("ul",class_="biglist")
    for juego in juegos:
        nombre = juego.find("div", class_="f_left with_two_rows").a.get("title").replace("™","").replace("®","")
        link = juego.find("div", class_="f_left with_two_rows").a.get("href")
        precio = juego.find_all("div", class_="f_right")[1].span.string
        imagen = juego.find_all("div", class_="f_left")[0].a.img.get("alt")
        nombres.append(nombre)
        links.append(link)
        precios.append(precio)
        imagenes.append(imagen)
