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
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='', unique=True)
    q = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_q')
    w = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_w')
    e = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_e')
    r = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_r')


class Hero(models.Model):
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE)
