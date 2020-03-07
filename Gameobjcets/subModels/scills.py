from .effects import *


class Skill(models.Model):
    name = models.CharField(max_length=40, default="")
    cooldown = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)


class SubSkill(models.Model):
    class Meta:
        abstract = True


class EffectsToTargetSubSkill(SubSkill):
    range = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    effects = models.OneToOneField(EffectPrototype, on_delete=models.CASCADE)
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)


class EffectsInZoneSubSkill(SubSkill):
    effects = models.OneToOneField(EffectPrototype, on_delete=models.CASCADE)
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)


class EffectsInRadiusSubSkill(SubSkill):
    range = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    effects = models.OneToOneField(EffectPrototype, on_delete=models.CASCADE)
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)
