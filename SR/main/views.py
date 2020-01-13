import shelve
from main.models import Libro, Puntuacion
from main.forms import UserForm, BookForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.populate import populateDatabase


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario)
        itemid = int(ra.book)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()
    


    
#  CONJUNTO DE VISTAS

def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')
 
# APARTADO D
def recommendedBooksUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            #user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            books = []
            scores = []
            for re in recommended:
                books.append(Book.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(books,scores)
            return render(request,'recommendationItems.html', {'idUsuario': idUser, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})

"""
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
"""

# APARTADO C
def similarBooks(request):
    book = None
    if request.method=='GET':
        form = BookForm(request.GET, request.FILES)
        if form.is_valid():
            idBook = form.cleaned_data['id']
            book = get_object_or_404(Book, pk=idBook)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idBook),n=2)
            books = []
            similar = []
            for re in recommended:
                books.append(Book.objects.get(pk=re[1]))
                similar.append(re[0])
            items= zip(books,similar)
            return render(request,'similarBooks.html', {'book': book,'books': items})
    form = BookForm()
    return render(request,'search_book.html', {'form': form})

"""
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

#APARTADO A
def search(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            #user = get_object_or_404(UserInformation, pk=idUser)
            booksVotedByUser = Puntuacion.objects.all().filter(idUsuario=idUser)
            books = []
            for ra in booksVotedByUser:
                books.append(Book.objects.get(idBook=ra.book.id))
            return render(request,'ratedBooks.html', {'idUsuario':idUser, 'books':books})
    form=UserForm()
    return render(request,'search_user.html', {'form':form })
