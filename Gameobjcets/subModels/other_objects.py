from django.db import models


class SolidObject(models.Model):
    pass


class Creature(SolidObject):
    class Meta:
        abstract = True


class Tower(SolidObject):
    pass


class Warrior(Creature):
    pass
