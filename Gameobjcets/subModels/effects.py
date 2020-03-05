from django.db import models

"""
Тут находятся модели эффектов, урона
"""


class Damage(models.Model):
    pass


class LevelsOnLevels(models.Model):
    pass


class EffectPrototype(models.Model):
    class Meta:
        abstract = True


# ------------------ subclasses
class AttackBuf(EffectPrototype):
    pass


class Slowdown(EffectPrototype):
    pass


class Stun(EffectPrototype):
    pass


class Fetter(EffectPrototype):
    pass


class Silence(EffectPrototype):
    pass


class Bleeding(EffectPrototype):
    pass


class Poisoning(EffectPrototype):
    pass


class Shield(EffectPrototype):
    pass


class Heal(EffectPrototype):
    pass
# -----------------------------


class Effect(models.Model):
    pass

