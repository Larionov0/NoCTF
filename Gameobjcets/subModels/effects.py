from django.db import models

"""
Тут находятся модели эффектов, урона
"""


class EffectCollector(models.Model):
    pass


class ValuesOnLevels(models.Model):
    lvl1 = models.IntegerField(default=-1)
    lvl2 = models.IntegerField(default=-1)
    lvl3 = models.IntegerField(default=-1)
    lvl4 = models.IntegerField(default=-1)
    lvl5 = models.IntegerField(default=-1)
    dop = models.CharField(default='', max_length=100, blank=True)


class Damage(models.Model):
    physical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='physical')
    magical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='magical')
    clear = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='clear')


class EffectPrototype(models.Model):
    live = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    is_instantly = False
    collector = models.ManyToManyField(EffectCollector)

    class Meta:
        abstract = True

    def create_effect(self):
        pass


# ------------------ subclasses
class AttackBuf(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="attack_buf_effect")


class Slowdown(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="slowdown_effect")


class Stun(EffectPrototype):
    pass


class Fetter(EffectPrototype):
    pass


class Silence(EffectPrototype):
    pass


class Bleeding(EffectPrototype):
    pass


class Poisoning(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="poisoning_effect")


class Shield(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="shield_effect")
    is_instantly = True


class Heal(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="heal_effect")
    is_instantly = True


# -----------------------------


class Effect(models.Model):
    live = models.IntegerField(default=0)
