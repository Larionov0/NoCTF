from django.db import models

"""
Тут находятся модели эффектов, урона
"""


class EffectCollector(models.Model):
    @property
    def effects(self):
        effects = []
        for set in filter(lambda set: set.endswith('_effects_set'), dir(self)):
            set = getattr(self, set)
            for effect in set.all():
                effects.append(effect)
        return effects


class ValuesOnLevels(models.Model):
    lvl1 = models.IntegerField(default=-1)
    lvl2 = models.IntegerField(default=-1)
    lvl3 = models.IntegerField(default=-1)
    lvl4 = models.IntegerField(default=-1)
    lvl5 = models.IntegerField(default=-1)
    dop = models.CharField(default='', max_length=100, blank=True)

    def __getitem__(self, number):
        if number == 1:
            return self.lvl1
        elif number == 2:
            return self.lvl2
        elif number == 3:
            return self.lvl3
        elif number == 4:
            return self.lvl4
        elif number == 5:
            return self.lvl5


class Damage(models.Model):
    physical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='physical')
    magical = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='magical')
    clear = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, blank=True, null=True, related_name='clear')


class Effect(models.Model):
    live = models.IntegerField(default=0)
    value = models.IntegerField(default=0)

    def tick(self):
        self.proto.tick(self.hero)
        self.minus_live()
        self.save()

    def minus_live(self):
        self.live -= 1
        self.save()
        if self.live <= 0:
            self.delete()

    def remove_from_hero(self):
        self.hero.remove_effect(self)
        if not self.proto.is_live_on_target:
            self.maker.remove_effect(self)

    @property
    def maker(self):
        return self.maker_set.all()[0]

    @property
    def hero(self):
        return self.hero_set.all()[0]

    @property
    def proto(self):
        for proto in self.get_all_prototypes():
            if self in proto.effects.all():
                return proto
        raise Exception(f"Effect without proto: {self}")

    def get_all_prototypes(self):
        protos = []
        for set in filter(lambda set: set.endswith('_proto'), dir(self)):
            set = getattr(self, set)
            for proto in set.all():
                protos.append(proto)
        return protos


class EffectPrototype(models.Model):
    is_live_on_target = True  # отсчет live во время хода игрока, НА КОТОРОМ еффект? (или игрока, который дал эфект)
    is_instantly = False

    live = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    collector = models.ManyToManyField(EffectCollector, blank=True, related_name='%(class)s_effects_set')
    effects = models.ManyToManyField(Effect, blank=True, related_name='%(class)s_proto')

    class Meta:
        abstract = True

    def create_effect(self):
        pass

    def tick(self, hero):
        pass

    @staticmethod
    def all_effect_prototypes():
        protos = []
        for cls in AttackBuf, Slowdown, Stun, Fetter, Silence, Bleeding, Poisoning, Shield, Heal:
            for proto in cls.objects.all():
                protos.append(proto)
        return protos


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
    value = 5

    def tick(self, hero):
        hero.get_damage(5)


class Poisoning(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="poisoning_effect")


class Shield(EffectPrototype):
    is_live_on_target = False
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="shield_effect")


class Heal(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="heal_effect")
    is_instantly = True


# -----------------------------
