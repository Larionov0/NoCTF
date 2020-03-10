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

    def tick(self, hero):
        self.proto.tick(hero)
        self.minus_live()
        self.save()

    def minus_live(self):
        self.live -= 1
        if self.live <= 0:
            self.hero.effects.remove(self)
        self.save()

    @property
    def proto(self):
        return self.proto.all()


class EffectPrototype(models.Model):
    live = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE)
    is_instantly = False
    collector = models.ManyToManyField(EffectCollector)
    effects = models.ManyToManyField(Effect, related_name='%(class)s_proto')

    class Meta:
        abstract = True

    def create_effect(self):
        pass

    def tick(self, hero):
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
    value = 5

    def tick(self, hero):
        hero.get_damage(5)


class Poisoning(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="poisoning_effect")


class Shield(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="shield_effect")
    is_instantly = True


class Heal(EffectPrototype):
    value = models.OneToOneField(ValuesOnLevels, on_delete=models.CASCADE, related_name="heal_effect")
    is_instantly = True


# -----------------------------
