from django.shortcuts import render, redirect
from django.template import RequestContext
from web.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# This defines the sorting algorithm used to sort items in a list by their name alphabetically
def alphabetize(element):
    # Return the element's name in lowercase which will allow python to sort item lists by their names alphabetically
    return element.name.lower()

# Create your views here.
def user_login(request):
    # This line is needed when passing information to a html page via render.
    context = RequestContext(request)
    # When user submits credentials...
    if request.method == 'POST':
        # Get the username and password given by user
        username = request.POST['username']
        password = request.POST['password']
        # Test if it is a valid user
        user = authenticate(request, username=username, password=password)
        # If a valid user is returned, log the user in. Otherwise, render error page.
        if user is not None:
            # Django function to log the user in
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'error.html', {'message' : "Invalid Login Credentials"}, context)
    # When user visits webpage via get display log in form.
    else:
        return render(request, 'login.html')

@login_required
def user_logout(request):
    # Django function to log the user out
    logout(request)
    return redirect('/')

def register(request):
    context = RequestContext(request)
    # This value is passed to the html which will allow it to decide between showing the register form or a success message.
    registered = False
    # If user submits credentials...
    if request.method == 'POST':
        # Get the user's inputs as form objects
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # Test for validity of inputs. For example, this will fail if another user has the username the registering user inputed
        if user_form.is_valid() and profile_form.is_valid():
            # save new user information
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            # Set registered to true so user will see a confirmation message
            registered = True
            # Log the user in automatically
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            login(request, user)
        else:
            return render(request, 'error.html', {'message' : "Invalid Register Credentials. Your username may already be taken."}, context)
    else:
        # Pass the values needed from userProfileForm to html so it can construct a image upload field
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'profile_form': profile_form, 'registered': registered}, context)

@login_required
def create_feats(request):
    context = RequestContext(request)
    # This value is passed to the html which will allow it to decide between showing the creation form or a success message. A similar structure is used in all of the create pages.
    created = False
    # If the form is submitted
    if request.method == 'POST':
        # Receive user input
        name = request.POST['name']
        featDescription = request.POST['featDescription']
        # Recieve user id from request
        userName = UserProfile.objects.get(user = request.user)
        # Create a new feat and save it
        f = Feat.objects.create(name=name, featDescription=featDescription, userName=userName)
        f.save
        # Set created to true so user will recieve a conformation message
        created = True
    return render(request, 'create_feats.html', {'created' : created}, context)

@login_required
def create_equipment(request):
    context = RequestContext(request)
    # Similar structure to create_feats, just with more user fields
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
    # Similar structure to create_feats, just with more user fields
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
    # Aquire user information
    userName = UserProfile.objects.get(user = request.user)
    # Aquire feats the user has created so the user may add them to this race
    feats = list(Feat.objects.filter(userName = userName))
    # This sort key is defined at the top of the document but to summarize it sorts elements by their name attribute alphabetically
    feats.sort(key=alphabetize)
    # Aquire spells the user has created so the user may add them to this race
    spells = list(Spell.objects.filter(userName = userName))
    spells.sort(key=alphabetize)
    if request.method == 'POST':
        name = request.POST['name']
        raceDescription = request.POST['raceDescription']
        # In addition to regular fields such as race and description, statMod is stored as a comma seperated list so all the three letter attributes must be combined
        STR = str(request.POST['STR'])
        DEX = str(request.POST['DEX'])
        CON = str(request.POST['CON'])
        INT = str(request.POST['INT'])
        WIS = str(request.POST['WIS'])
        CHA = str(request.POST['CHA'])
        statMod = STR + ", " + DEX + ", " + CON + ", " + INT + ", " + WIS + ", " + CHA
        # When the user selects a feat they want a race to have the post request will be 'racefeats' and then the id of the feat. This block of code allows us to see which feats the user picked.
        raceFeats = ""
        # Go through all the feats the user has created and see if a post request was sent with the right id (AKA the user selected that feat)
        for f in feats:
            query = 'raceFeats' + str(f.id)
            # If the query exsists add it's id to raceFeats
            if query in request.POST:
                raceFeats += str(request.POST[query]) + ","
        # Remove the extra trailing comma
        raceFeats = raceFeats.strip(",")
        # This functions like feats do
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
    # In addition to the regular created variable, feats and spells must also be passed in so the user can see what choices of feats and spells they have.
    return render(request, 'create_races.html', {'created' : created, 'feats' : feats, 'spells' : spells}, context)

@login_required
def create_classes(request):
    context = RequestContext(request)
    # Behaves very similar to races
    created = False
    userName = UserProfile.objects.get(user = request.user)
    feats = list(Feat.objects.filter(userName = userName))
    feats.sort(key=alphabetize)
    # Gets the items the user has created
    items = list(EquipmentItem.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    if request.method == 'POST':
        name = request.POST['name']
        classDescription = request.POST['classDescription']
        classProficiencyBonus = request.POST['classProficiencyBonus']
        classFamily = request.POST['classFamily']
        classLevel = request.POST['classLevel']
        classHitDice = request.POST['classHitDice']
        # Behaves like race's statMod
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
        # Behaves like spells and feats in races
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
    # Once again items and feats must be passed to user so they can pick from those options
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
    # In addition to feats, items and spells, the user picks races and classes for the character. That being said this process is very similar to create_races and create_classes
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
        # Unlike other fields, there must be exactly one race inputted by the user. It is possible to submit the form without selecting a race so if that happens, the user will recieve an error.
        if 'advRace' not in request.POST:
            return render(request, 'error.html', {'message' : "No Race Selected."}, context)
        # Because only one race is selected it's request.POST can be called simply advRace and can be directly applied to advRace. Notice also that unlike things like class, advRace is actually a race object, not an id.
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
    # Feats, spells, items, races and classLevels (aka classes) must all be sent to the html to provide the user with options
    return render(request, 'create_characters.html', {'created' : created, 'feats' : feats, 'spells' : spells, 'items' : items, 'races' : races, 'classLevels' : classLevels}, context)

# The main page. This is where yu will be sent if you type in a undefined url (see web/urls.py)
def index(request):
    return render(request, 'index.html')

# This page lets you access all of the create pages
@login_required
def create(request):
    return render(request, 'create.html')

# This page lets you access all of the pages where you can view your creations
@login_required
def view(request):
    return render(request, 'view.html')

# All the pages below this point let the user view things they have already created in table form. Additionally,
@login_required
def feats(request):
    context = RequestContext(request)
    # If the user presses delete the id of the item they want to delete is sent here and the item is removed from the database.
    if request.method == 'POST':
        delete = Feat.objects.get(id = request.POST['delete'])
        delete.delete()
    userName = UserProfile.objects.get(user = request.user)
    # In this case items does not stand for equipment items but rather is a generic term for the results pulled when the view pages find the items the user has created (in this case feats).
    items = list(Feat.objects.filter(userName = userName))
    items.sort(key=alphabetize)
    # Once again the items sent to the html are not equipment items but are instead the collection of table rows
    return render(request, 'feats.html', {'items' : items}, context)

@login_required
def equipment(request):
    # Similar structure to feats
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
    # Similar structure to feats and equipment
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
    # Similar to above view pages but now every item's feats and spells must be converted from id to name
    for item in items:
        raceFeats = ""
        # If the race has feats the comma seperated values are split up into a list
        if not item.raceFeats == "":
            feats = item.raceFeats.split(",")
            # For each id in the list it's corresponding feat is found
            for f in feats:
                feat = Feat.objects.get(id = f)
                # The name of this feat is added to raceFeats string
                raceFeats += feat.name + ", "
            # raceFeats is updated from a comma seperated id string to a comma seperated name string that the user can understand
            item.raceFeats = raceFeats.strip(", ")
        # Behaves like raceFeats
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
        # Although this behaves very similar to classFeats, raceFeats, and raceSpells, the use of "item" can make this a bit confusing to read so the variables used will be explicitly defined to improve readability. classEquipment is the string that will hold the names of the equipment the class has.
        classEquipment = ""
        # If the item's (class instance's) classItems (the list of ids representing equipment the class has) is not empty...
        if not item.classItems == "":
            # Here we define eItems as a list of ids received from splitting item.classItems by comma
            eItems = item.classItems.split(",")
            # For each e (individual equipment id) in eItems
            for e in eItems:
                # Here we define equipmentItem as an individual EqquipmentItem with the id of e
                equipmentItem = EquipmentItem.objects.get(id = e)
                # We add the name of equipmentItem to classEquipment
                classEquipment += equipmentItem.name + ", "
            # Finally we complete the last step of removing the trailing comma before turning item.classItems from a comma seperated id string to a comma seperated name string.
            item.classItems = classEquipment.strip(", ")
    return render(request, 'classes.html', {'items' : items}, context)

@login_required
def characters(request):
    context = RequestContext(request)
    # This behaves like all the above veiw pages, just with more values.
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

# This is where you can view the characters as a single page in more detail then characters provides.
@login_required
def viewer(request):
    context = RequestContext(request)
    # You can only access this page by clicking on the expand button in characters
    if request.method == 'GET':
        return redirect('/characters')
    # If you click on the expand button in characters...
    if request.method == 'POST':
        # We begin by simply accessing the character and race using the id passed by the expand button
        character = Adventurer.objects.get(id = request.POST['expand'])
        race = character.advRace
        # Here we determine the adventurer's final stats by combining the race stat mod with the base stats
        advStats = character.advStats.split(",")
        raceStats = race.statMod.split(",")
        stats = []
        # We add each stat to the stat mod and the result is sent to stats
        for stat in range(len(advStats)):
            stats.append(int(advStats[stat]) + int(raceStats[stat]))
        # Classes are a bit more complex as a player can have multiple classes and it is possible that some of the classes they picked are redundant (ex. Bard level 2 and Bard Level 1) or are minimal and thereby missing information (only Bard level 2). First we begin by creating an empty list which will hold all of our classes at the end of the process.
        classes = []
        # Then we create a set to hold the id of feats provided by our classes
        classFeats = set()
        # If the character has at least one class...
        if not character.advClass == "":
            # split the string of comma seperated class ids into a list called classLevels
            classLevels = character.advClass.split(",")
            # for each class id in classLevels (which has an index of c in the list)...
            for c in range(len(classLevels)):
                # get the class associated with the id and call it classLevel
                classLevel = AdventurerClassLevel.objects.get(id = classLevels[c])
                # get it's family
                family = classLevel.classFamily
                # check to see if the user has made any other classes in the same family.
                otherClasses = AdventurerClassLevel.objects.filter(classFamily = family)
                # for each other class in the same family (o)
                for o in otherClasses:
                    # If the other classes have a level less than the current class's level
                    if o.classLevel < classLevel.classLevel:
                        # merge the feats from the lower class into the feat list
                        classFeats = classFeats | set(o.classFeats.split(","))
                        # if the level of that other class in the family is 1...
                        if o.classLevel == 1:
                            # Set class items, description and Proficiencies to that of the base class
                            classLevel.classItems = o.classItems
                            classLevel.classDescription = o.classDescription
                            classLevel.classProficiencies = o.classProficiencies
                # Add this class
                classes.append(classLevel)
                # Add the feats this class has (It is a set so it is okay if there is redundancy)
                classFeats = classFeats | set(classLevel.classFeats.split(","))
                # Now we check all the other classes this adventurer has
                for cl in classLevels:
                    altClassLevel = AdventurerClassLevel.objects.get(id = cl)
                    # If the adventurer has two classes in the same family, we only need to display the highest leveled class of that family so we remove the lesser one from classes list.
                    if family == altClassLevel.classFamily and altClassLevel.classLevel > classLevel.classLevel:
                        classes.pop(c)
                        break
        # Now we find the feats provided by the race and the adventurer's bonus feats
        advFeats = set(character.advFeats.split(","))
        raceFeats = set(race.raceFeats.split(","))
        # Now we merge all of the feat ids into one master set
        totalFeats = advFeats | raceFeats | classFeats
        # this lines converts total feats into a list while also removing any "" that can occur if one of the three Feat sets was empty (example: if a race had no feats)
        totalFeats = [x for x in totalFeats if x != ""]
        # Then we find the feats associated with the ids and add them to a list of feat objects
        feats = list()
        for f in totalFeats:
            feat = Feat.objects.get(id = f)
            feats.append(feat)
        # Spells behave much like how advFeats and raceFeats did.
        advSpells = set(character.advSpells.split(","))
        raceSpells = set(race.raceSpells.split(","))
        totalSpells = advSpells | raceSpells
        totalSpells = [x for x in totalSpells if x != ""]
        spells = list()
        for s in totalSpells:
            spell = Spell.objects.get(id = s)
            spells.append(spell)
        # Items behave like spells but with the exception of first merging all the items from all of the classes into one classItems set
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
        # Then, we sort all the lists using alphabetize
        classes.sort(key=alphabetize)
        feats.sort(key=alphabetize)
        spells.sort(key=alphabetize)
        items.sort(key=alphabetize)
        # Finally we render the page passing in all the nessecary values.
        return render(request, 'viewer.html', {'character' : character, 'race' : race, 'classes' : classes, 'feats' : feats, 'spells' : spells, 'items' : items, 'stats' : stats}, context)
