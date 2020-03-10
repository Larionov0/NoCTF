from django.contrib import admin
from .models import *

# Register your models here.
for cls in HeroPrototype, Hero, Stats, ValuesOnLevels, Skill, StatBubble, PriceBubble:
    admin.site.register(cls)
