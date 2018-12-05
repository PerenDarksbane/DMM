from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class AdventurerClassLevel(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    classFamily = models.CharField(max_length=50)
    classDescription = models.TextField()
    classProficiencyBonus = models.PositiveSmallIntegerField()
    classLevel = models.PositiveSmallIntegerField()
    classHitDice = models.CharField(max_length=50)
    classFeats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    classSpellslots = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    classItems = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    classProficiencies = models.TextField()

class AdventurerRace(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    raceDescription = models.TextField()
    raceFeats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    raceSpells = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    raceSize = models.CharField(max_length=50)
    raceSpeed = models.CharField(max_length=50)
    statMod = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    raceProficiencies = models.TextField()

class Feat(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    featDescription = models.TextField()

class Spell(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    spellDescription = models.TextField()
    spellLevel = models.PositiveSmallIntegerField()
    spellCastTime = models.CharField(max_length=50)
    spellRange = models.CharField(max_length=100)
    spellComponents = models.TextField()
    spellDuration = models.CharField(max_length=50)

class EquipmentItem(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    itemDescription = models.TextField()
    itemRarity = models.CharField(max_length=50)

class Adventurer(models.Model):
    userName = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    advBackground = models.TextField()
    advClass = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    advRace = models.ForeignKey(AdventurerRace, on_delete=models.CASCADE)
    advFeats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    advItems = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    advSpells = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    advStats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
