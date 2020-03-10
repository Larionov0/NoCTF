from .scills import *


class AbstractBubble(models.Model):
    vaule = models.IntegerField(default=0)
    class Meta:
        abstract = True


class PriceBubble(AbstractBubble):
    pass


class StatBubble(AbstractBubble):
    next = models.OneToOneField(PriceBubble, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name="prev_bubble")
    prev = models.OneToOneField(PriceBubble, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='next_bubble')


class Stats(models.Model):
    attack = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name="attack_stats")
    magic = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="magic_stats")
    armor = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="armor_stats")
    range = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="range_stats")
    speed = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="speed_stats")


class HeroPrototype(models.Model):
    name = models.CharField(max_length=30, default='', unique=True)
    hp = models.OneToOneField(ValuesOnLevels, on_delete=models.SET_NULL, null=True, blank=True)
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE)
    q = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_q')
    w = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_w')
    e = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_e')
    r = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_r')


class Hero(models.Model):
    proto = models.ForeignKey(HeroPrototype, on_delete=models.CASCADE)
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE)
    hp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_alive = models.BooleanField(default=True)
    effects = models.ForeignKey(Effect, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero')

    def change_hp(self, hp):
        if hp >= 0:
            return self.get_heal(hp)
        else:
            return self.get_damage(-hp)

    def get_damage(self, hp):
        assert hp >= 0
        self.hp -= hp
        if self.hp <= 0:
            self.is_alive = False
        self.save()

    def get_heal(self, hp):
        assert hp >= 0
        self.hp += hp
        max_hp = self.max_hp
        if self.hp > max_hp:
            self.hp = max_hp
        self.save()

    def tick(self):
        for effect in self.effects:
            effect.tick(self)

    @property
    def max_hp(self):
        return self.proto.hp[self.level]
