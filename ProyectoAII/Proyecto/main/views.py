import shelve
from main.models import User, Game, Offer, Tag
from main.forms import UserForm, GameForm, TagForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.populate import populateGamesDatabase

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
    populateGamesDatabase() 
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
            game = Game.objects.filter(name__contains=name)
            if len(game) == 0:
                form=UserForm()
                return render(request,'search_user.html', {'form':form })
            elif len(game) == 1:
                offers = Offer.objects.get(idGame=game.idGame)
                return render(request,'offer_list.html', {'offers':offers })
            else:
                return render(request,'games.html', {'games':game })

        else:
            form=UserForm()
            return render(request,'search_user.html', {'form':form })


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

def instantgaming(juego):
    nombres = []
    links = []
    descuentos = []
    precios = []
    imagenes = []
    site = "https://www.instant-gaming.com/en/search/?q="+str(juego)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    juegos = soup.find("div",class_="search")
    for juego in juegos:
        if isinstance(juego, NavigableString):
            continue
        nombre = juego.find("div",class_="name").string
        nombres.append(nombre)
        a = juego.find("a")
        link = a.get("href")
        links.append(link)
        try:
            descuento = a.find("div",class_="discount").string
        except:
            descuento = "0%"
        descuentos.append(descuento)
        precio = a.find("div", class_="price").string
        precios.append(precio)
        imagen = a.find("img").get("src")
        imagenes.append(imagen)
        
    return nombres,links,descuentos,imagenes
