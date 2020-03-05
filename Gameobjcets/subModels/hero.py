from .scills import *


class HeroPrototype(models.Model):
    pass


class Hero(models.Model):
    pass


class Stats(models.Model):
    pass


class AbstractBubble(models.Model):
    class Meta:
        abstract = True


class StatBubble(AbstractBubble):
    pass


class PriceBubble(AbstractBubble):
    pass
