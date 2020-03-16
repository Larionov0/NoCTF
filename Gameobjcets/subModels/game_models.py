from .hero import *


class Game(models.Model):
    teams = models.ManyToManyField(Team, related_name='%(class)s_game_MY')
    turn = models.OneToOneField(Hero, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True



class StandardGame(Game):
    pass
