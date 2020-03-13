from .effects import *


class Skill(models.Model):
    name = models.CharField(max_length=40, default="")
    cooldown = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)


class SubSkill(models.Model):
    effects_collector = models.OneToOneField(EffectCollector, on_delete=models.CASCADE,
                                             related_name='%(class)s_one_MY')  # ПОка не знаю, как нормально реализовать обратное имя

    class Meta:
        abstract = True

    def hang_effects_to_target(self, target):
        for effect in self.effects:
            target.add_effect(effect)

    @property
    def effects(self):
        return self.effects_collector.effects


class EffectsToTargetSubSkill(SubSkill):
    range = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)


class EffectsInZoneSubSkill(SubSkill):
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)


class EffectsInRadiusSubSkill(SubSkill):
    range = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    damage = models.OneToOneField(Damage, on_delete=models.CASCADE)
