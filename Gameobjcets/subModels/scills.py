from .effects import *


class Skill(models.Model):
    pass


class SubSkill(models.Model):
    class Meta:
        abstract = True


class EffectsToTargetSubSkill(SubSkill):
    pass


class EffectsInZoneSubSkill(SubSkill):
    pass


class EffectsInRadiusSubSkill(SubSkill):
    pass
