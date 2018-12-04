from django.shortcuts import render, redirect
from django.template import RequestContext
from web.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def alphabetize(element):
    return element.name.lower()

# Create your views here.
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')
    else:
        return render(request, 'login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(
            request,
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

@login_required
def create_feat(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        name = request.POST['name']
        featDescription = request.POST['featDescription']
        userName = UserProfile.objects.get(user = request.user)
        f = Feat.objects.create(name=name, featDescription=featDescription, userName=userName)
        f.save
        created = True
    return render(request, 'create_feat.html', {'created' : created}, context)

@login_required
def create_equipment(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        name = request.POST['name']
        itemDescription = request.POST['itemDescription']
        itemRarity = request.POST['itemRarity']
        userName = UserProfile.objects.get(user = request.user)
        f = EquipmentItem.objects.create(name=name, itemDescription=itemDescription, itemRarity=itemRarity, userName=userName)
        f.save
        created = True
    return render(request, 'create_equipment.html', {'created' : created}, context)

@login_required
def create_spells(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        name = request.POST['name']
        spellDescription = request.POST['spellDescription']
        spellLevel = request.POST['spellLevel']
        spellCastTime = request.POST['spellCastTime']
        spellRange = request.POST['spellRange']
        spellComponents = request.POST['spellComponents']
        spellDuration = request.POST['spellDuration']
        userName = UserProfile.objects.get(user = request.user)
        f = Spell.objects.create(name=name, spellDescription=spellDescription, spellLevel=spellLevel, spellCastTime=spellCastTime, spellRange=spellRange, spellComponents=spellComponents, spellDuration=spellDuration, userName=userName)
        f.save
        created = True
    return render(request, 'create_spells.html', {'created' : created}, context)

def index(request):
    return render(request, 'index.html')

@login_required
def create(request):
    return render(request, 'create.html')

@login_required
def view(request):
    return render(request, 'view.html')

@login_required
def feats(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = Feat.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(Feat.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    return render(request, 'feats.html', {'items' : items}, context)

@login_required
def equipment(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = EquipmentItem.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(EquipmentItem.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    return render(request, 'equipment.html', {'items' : items}, context)

@login_required
def spells(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = Spell.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(Spell.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    return render(request, 'spells.html', {'items' : items}, context)
