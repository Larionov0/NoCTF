from django.db import models

"""
Тут находятся модели эффектов, урона
"""


class ValuesOnLevels(models.Model):
    lvl1 = models.IntegerField(default=-1)
    lvl2 = models.IntegerField(default=-1)
    lvl3 = models.IntegerField(default=-1)
    lvl4 = models.IntegerField(default=-1)
    lvl5 = models.IntegerField(default=-1)
    dop = models.CharField(default='', blank=True)


class Damage(models.Model):
    physical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='physical')
    magical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='magical')
    clear = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='clear')


class EffectPrototype(models.Model):
    live = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    is_instantly = False

    class Meta:
        abstract = True

    def create_effect(self):
        pass


# ------------------ subclasses
class AttackBuf(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)


class Slowdown(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)


class Stun(EffectPrototype):
    pass


class Fetter(EffectPrototype):
    pass


class Silence(EffectPrototype):
    pass


class Bleeding(EffectPrototype):
    pass


class Poisoning(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)


class Shield(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    is_instantly = True


class Heal(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    is_instantly = True


# -----------------------------


class Effect(models.Model):
    live = models.IntegerField(default=0)
