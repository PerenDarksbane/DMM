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
        e = EquipmentItem.objects.create(name=name, itemDescription=itemDescription, itemRarity=itemRarity, userName=userName)
        e.save
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
        s = Spell.objects.create(name=name, spellDescription=spellDescription, spellLevel=spellLevel, spellCastTime=spellCastTime, spellRange=spellRange, spellComponents=spellComponents, spellDuration=spellDuration, userName=userName)
        s.save
        created = True
    return render(request, 'create_spells.html', {'created' : created}, context)

@login_required
def create_races(request):
    context = RequestContext(request)
    created = False
    userName = UserProfile.objects.get(user = request.user)
    feats = list(Feat.objects.filter(userName = userName))
    feats.sort(key=alphabetize)
    spells = list(Spell.objects.filter(userName = userName))
    spells.sort(key=alphabetize)
    if request.method == 'POST':
        name = request.POST['name']
        raceDescription = request.POST['raceDescription']
        STR = str(request.POST['STR'])
        DEX = str(request.POST['DEX'])
        CON = str(request.POST['CON'])
        INT = str(request.POST['INT'])
        WIS = str(request.POST['WIS'])
        CHA = str(request.POST['CHA'])
        statMod = STR + ", " + DEX + ", " + CON + ", " + INT + ", " + WIS + ", " + CHA
        raceFeats = ""
        for f in feats:
            query = 'raceFeats' + str(f.id)
            if query in request.POST:
                raceFeats += str(request.POST[query]) + ","
        raceFeats = raceFeats.strip(",")
        raceSpells = ""
        for s in spells:
            query = 'raceSpells' + str(s.id)
            if query in request.POST:
                raceSpells += str(request.POST[query]) + ","
        raceSpells = raceSpells.strip(",")
        raceSize = request.POST["raceSize"]
        raceSpeed = request.POST["raceSpeed"]
        raceProficiencies = request.POST["raceProficiencies"]
        userName = UserProfile.objects.get(user = request.user)
        r = AdventurerRace.objects.create(name=name, raceDescription=raceDescription, statMod=statMod, raceFeats=raceFeats, raceSpells=raceSpells, raceSize=raceSize, raceSpeed=raceSpeed, raceProficiencies=raceProficiencies, userName=userName)
        r.save
        created = True
    return render(request, 'create_races.html', {'created' : created, 'feats' : feats, 'spells' : spells}, context)

@login_required
def create_classes(request):
    context = RequestContext(request)
    created = False
    userName = UserProfile.objects.get(user = request.user)
    feats = list(Feat.objects.filter(userName = userName))
    feats.sort(key=alphabetize)
    items = list(EquipmentItem.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    if request.method == 'POST':
        name = request.POST['name']
        classDescription = request.POST['classDescription']
        classProficiencyBonus = request.POST['classProficiencyBonus']
        classFamily = request.POST['classFamily']
        classLevel = request.POST['classLevel']
        classHitDice = request.POST['classHitDice']
        SS0 = str(request.POST['0'])
        SS1 = str(request.POST['1'])
        SS2 = str(request.POST['2'])
        SS3 = str(request.POST['3'])
        SS4 = str(request.POST['4'])
        SS5 = str(request.POST['5'])
        SS6 = str(request.POST['6'])
        SS7 = str(request.POST['7'])
        SS8 = str(request.POST['8'])
        SS9 = str(request.POST['9'])
        classSpellslots = SS0 + ", " + SS1 + ", " + SS2 + ", " + SS3 + ", " + SS4 + ", " + SS5 + ", " + SS6 + ", " + SS7 + ", " + SS8 + ", " + SS9
        classFeats = ""
        for f in feats:
            query = 'classFeats' + str(f.id)
            if query in request.POST:
                classFeats += str(request.POST[query]) + ","
        classFeats = classFeats.strip(",")
        classItems = ""
        for i in items:
            query = 'classItems' + str(i.id)
            if query in request.POST:
                classItems += str(request.POST[query]) + ","
        classItems = classItems.strip(",")
        classProficiencies = request.POST["classProficiencies"]
        userName = UserProfile.objects.get(user = request.user)
        r = AdventurerClassLevel.objects.create(name=name, classDescription=classDescription, classProficiencyBonus=classProficiencyBonus, classFamily=classFamily, classLevel=classLevel, classHitDice=classHitDice, classSpellslots=classSpellslots, classFeats=classFeats, classItems=classItems, classProficiencies=classProficiencies, userName=userName)
        r.save
        created = True
    return render(request, 'create_classes.html', {'created' : created, 'feats' : feats, 'items' : items}, context)

@login_required
def create_characters(request):
    context = RequestContext(request)
    created = False
    userName = UserProfile.objects.get(user = request.user)
    feats = list(Feat.objects.filter(userName = userName))
    feats.sort(key=alphabetize)
    spells = list(Spell.objects.filter(userName = userName))
    spells.sort(key=alphabetize)
    items = list(EquipmentItem.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    races = list(AdventurerRace.objects.filter(userName = userName))
    races.sort(key=alphabetize)
    classLevels = list(AdventurerClassLevel.objects.filter(userName = userName))
    classLevels.sort(key=alphabetize)
    if request.method == 'POST':
        name = request.POST['name']
        advBackground = request.POST['advBackground']
        STR = str(request.POST['STR'])
        DEX = str(request.POST['DEX'])
        CON = str(request.POST['CON'])
        INT = str(request.POST['INT'])
        WIS = str(request.POST['WIS'])
        CHA = str(request.POST['CHA'])
        advStats = STR + ", " + DEX + ", " + CON + ", " + INT + ", " + WIS + ", " + CHA
        advFeats = ""
        for f in feats:
            query = 'advFeats' + str(f.id)
            if query in request.POST:
                advFeats += str(request.POST[query]) + ","
        advFeats = advFeats.strip(",")
        advSpells = ""
        for s in spells:
            query = 'advSpells' + str(s.id)
            if query in request.POST:
                advSpells += str(request.POST[query]) + ","
        advSpells = advSpells.strip(",")
        advItems = ""
        for i in items:
            query = 'advItems' + str(i.id)
            if query in request.POST:
                advItems += str(request.POST[query]) + ","
        advItems = advItems.strip(",")
        if 'advRace' not in request.POST:
            return render(request, 'error.html', {'message' : "No race selected."}, context)
        advRace = AdventurerRace.objects.get(id=request.POST['advRace'])
        advClass = ""
        for c in classLevels:
            query = 'advClass' + str(c.id)
            if query in request.POST:
                advClass += str(request.POST[query]) + ","
        advClass = advClass.strip(",")
        userName = UserProfile.objects.get(user = request.user)
        r = Adventurer.objects.create(name=name, advBackground=advBackground, advStats=advStats, advFeats=advFeats, advSpells=advSpells, advItems=advItems, advRace=advRace, advClass=advClass, userName=userName)
        r.save
        created = True
    return render(request, 'create_characters.html', {'created' : created, 'feats' : feats, 'spells' : spells, 'items' : items, 'races' : races, 'classLevels' : classLevels}, context)

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

@login_required
def races(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = AdventurerRace.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(AdventurerRace.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    for item in items:
        raceFeats = ""
        if not item.raceFeats == "":
            feats = item.raceFeats.split(",")
            for f in feats:
                feat = Feat.objects.get(id = f)
                raceFeats += feat.name + ", "
            item.raceFeats = raceFeats.strip(", ")
        raceSpells = ""
        if not item.raceSpells == "":
            spells = item.raceSpells.split(",")
            for s in spells:
                spell = Spell.objects.get(id = s)
                raceSpells += spell.name + ", "
            item.raceSpells = raceSpells.strip(", ")
    return render(request, 'races.html', {'items' : items}, context)

@login_required
def classes(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = AdventurerClassLevel.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(AdventurerClassLevel.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    for item in items:
        classFeats = ""
        if not item.classFeats == "":
            feats = item.classFeats.split(",")
            for f in feats:
                feat = Feat.objects.get(id = f)
                classFeats += feat.name + ", "
            item.classFeats = classFeats.strip(", ")
        classEquipment = ""
        if not item.classItems == "":
            eItems = item.classItems.split(",")
            for e in eItems:
                equipmentItem = EquipmentItem.objects.get(id = e)
                classEquipment += equipmentItem.name + ", "
            item.classItems = classEquipment.strip(", ")
    return render(request, 'classes.html', {'items' : items}, context)

@login_required
def characters(request):
    context = RequestContext(request)
    if request.method == 'POST':
        delete = Adventurer.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    items = list(Adventurer.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    for item in items:
        advFeats = ""
        if not item.advFeats == "":
            feats = item.advFeats.split(",")
            for f in feats:
                feat = Feat.objects.get(id = f)
                advFeats += feat.name + ", "
            item.advFeats = advFeats.strip(", ")
        advEquipment = ""
        if not item.advItems == "":
            eItems = item.advItems.split(",")
            for e in eItems:
                equipmentItem = EquipmentItem.objects.get(id = e)
                advEquipment += equipmentItem.name + ", "
            item.advItems = advEquipment.strip(", ")
        advSpells = ""
        if not item.advSpells == "":
            spells = item.advSpells.split(",")
            for s in spells:
                spell = Spell.objects.get(id = s)
                advSpells += spell.name + ", "
            item.advSpells = advSpells.strip(", ")
        advClass = ""
        if not item.advClass == "":
            classLevels = item.advClass.split(",")
            for c in classLevels:
                classLevel = AdventurerClassLevel.objects.get(id = c)
                advClass += classLevel.name + ", "
            item.advClass = advClass.strip(", ")
    return render(request, 'characters.html', {'items' : items}, context)

@login_required
def viewer(request):
    context = RequestContext(request)
    if request.method == 'GET':
        return redirect('/characters')
    if request.method == 'POST':
        character = Adventurer.objects.get(id = request.POST['expand'])
        race = character.advRace
        classes = []
        classFeats = set()
        if not character.advClass == "":
            classLevels = character.advClass.split(",")
            for c in range(len(classLevels)):
                classLevel = AdventurerClassLevel.objects.get(id = classLevels[c])
                family = classLevel.classFamily
                otherClasses = AdventurerClassLevel.objects.filter(classFamily = family)
                for o in otherClasses:
                    if o.classLevel == 1:
                        classFeats = classFeats | set(classLevel.classFeats.split(","))
                        for f in o.classFeats.split(","):
                            classFeats.add(f)
                            classLevel.classFeats = classFeats
                            classLevel.classItems = o.classItems
                            classLevel.classDescription = o.classDescription
                            classLevel.classProficiencies= o.classProficiencies
                classes.append(classLevel)
                for cl in classLevels:
                    altClassLevel = AdventurerClassLevel.objects.get(id = cl)
                    if family == altClassLevel.classFamily and altClassLevel.classLevel > classLevel.classLevel:
                        classes.pop(c)
                        break
        advFeats = set(character.advFeats.split(","))
        raceFeats = set(race.raceFeats.split(","))
        totalFeats = advFeats | raceFeats | classFeats
        totalFeats = [x for x in totalFeats if x != ""]
        feats = list()
        for f in totalFeats:
            feat = Feat.objects.get(id = f)
            feats.append(feat)
        advSpells = set(character.advSpells.split(","))
        raceSpells = set(race.raceSpells.split(","))
        totalSpells = advSpells | raceSpells
        totalSpells = [x for x in totalSpells if x != ""]
        spells = list()
        for s in totalSpells:
            spell = Spell.objects.get(id = s)
            spells.append(spell)
        advItems = set(character.advItems.split(","))
        classItems = set()
        for classLevel in classes:
            classItems = classItems | set(classLevel.classItems.split(","))
        totalItems = classItems | advItems
        totalItems = [x for x in totalItems if x != ""]
        items = list()
        for i in totalItems:
            item = EquipmentItem.objects.get(id = i)
            items.append(item)
        classes.sort(key=alphabetize)
        feats.sort(key=alphabetize)
        spells.sort(key=alphabetize)
        items.sort(key=alphabetize)
        return render(request, 'viewer.html', {'character' : character, 'race' : race, 'classes' : classes, 'feats' : feats, 'spells' : spells, 'items' : items}, context)
