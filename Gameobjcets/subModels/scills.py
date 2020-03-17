from .effects import *


class Skill(models.Model):
    name = models.CharField(max_length=40, default="")
    cooldown = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)

    def __str__(self):
        return f"Skill {self.name}"

    @property
    def sub_skills(self):
        sub_skills = []
        for attr in filter(lambda attr: attr.endswith('_subskills_MY'), dir(self)):
            set_ = getattr(self, attr).all()
            for sub_skill in set_:
                sub_skills.append(sub_skill)
        return sub_skills


class SubSkill(models.Model):
    effects_collector = models.OneToOneField(EffectCollector, on_delete=models.CASCADE,
                                             related_name='%(class)s_one_MY')  # ПОка не знаю, как нормально реализовать обратное имя
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="%(class)s_subskills_MY")

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
