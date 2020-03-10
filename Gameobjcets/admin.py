from django.contrib import admin
from .models import *

# Register your models here.
for cls in HeroPrototype, Hero, Stats, ValuesOnLevels, Skill, StatBubble, PriceBubble, Effect:
    admin.site.register(cls)

for cls in Heal, Poisoning:
    admin.site.register(cls)
