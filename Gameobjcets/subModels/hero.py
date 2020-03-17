from .scills import *


class AbstractBubble(models.Model):
    value = models.IntegerField(default=0)

    class Meta:
        abstract = True


class PriceBubble(AbstractBubble):
    def __str__(self):
        return f"PriceBubble {self.value}"


class StatBubble(AbstractBubble):
    next = models.OneToOneField(PriceBubble, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name="prev_bubble")
    prev = models.OneToOneField(PriceBubble, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='next_bubble')

    def __str__(self):
        return f"StatBubble {self.value}"

    @classmethod
    def create_base(cls):
        ob = cls.objects.create(value=0)
        ob.save()
        return ob


class Stats(models.Model):
    attack = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name="attack_stat")
    magic = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="magic_stat")
    armor = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="armor_stat")
    range = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="range_stat")
    speed = models.ForeignKey(StatBubble, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name="speed_stat")

    def __str__(self):
        return f"at {self.attack.value}; m {self.magic.value}; ar {self.armor.value}; r {self.range.value}; s {self.speed.value}"

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @classmethod
    def create_copy(cls, other):
        new_stats = cls.objects.create()
        new_stats.attack = other.attack
        new_stats.magic = other.magic
        new_stats.armor = other.armor
        new_stats.range = other.range
        new_stats.speed = other.speed
        new_stats.save()
        return new_stats

    @classmethod
    def create_base(cls):
        new_stats = cls.objects.create()
        new_stats.attack = StatBubble.create_base()
        new_stats.magic = StatBubble.create_base()
        new_stats.armor = StatBubble.create_base()
        new_stats.range = StatBubble.create_base()
        new_stats.speed = StatBubble.create_base()
        new_stats.save()
        return new_stats

    def delete_with_bubbles(self):
        self.attack.delete()
        self.magic.delete()
        self.armor.delete()
        self.range.delete()
        self.speed.delete()
        self.delete()


class Team(models.Model):
    @property
    def game(self):
        for set in filter(lambda set: set.endswith('_game_MY'), dir(self)):
            set = getattr(self, set)
            if len(set.all()) != 0:
                return set.all()[0]


class HeroPrototype(models.Model):
    name = models.CharField(max_length=30, default='', unique=True)
    hp = models.OneToOneField(ValuesOnLevels, on_delete=models.SET_NULL, null=True, blank=True)
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE)
    q = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_q')
    w = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_w')
    e = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_e')
    r = models.OneToOneField(Skill, on_delete=models.SET_NULL, blank=True, null=True, related_name='hero_r')

    def __str__(self):
        return f"HeroProto {self.name}"

    def create_hero(self):
        stats = Stats.create_copy(self.stats)

        skills = SkillsCooldowns(
            q=self.q,
            w=self.w,
            e=self.e,
            r=self.r
        )
        skills.save()

        hero = Hero.objects.create(
            proto=self,
            stats=stats,
            modifier=Stats.create_base(),
            skills=skills
        )
        hero.init()


class SkillsCooldowns(models.Model):
    q_cooldown = models.IntegerField(default=0)
    w_cooldown = models.IntegerField(default=0)
    e_cooldown = models.IntegerField(default=0)
    r_cooldown = models.IntegerField(default=0)
    q = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='q_MY')
    w = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='w_MY')
    e = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='e_MY')
    r = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='r_MY')


class Hero(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    proto = models.ForeignKey(HeroPrototype, on_delete=models.CASCADE)
    stats = models.OneToOneField(Stats, on_delete=models.CASCADE, related_name='hero_stats')
    modifier = models.OneToOneField(Stats, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='hero_modifier')
    hp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_alive = models.BooleanField(default=True)
    effects = models.ManyToManyField(Effect, blank=True)
    my_effects = models.ManyToManyField(Effect, blank=True, related_name='maker_set')
    energy_on_this_move = models.FloatField(default=0)
    skills = models.OneToOneField(SkillsCooldowns, on_delete=models.SET_NULL, blank=True, null=True)

    def init(self):
        self.hp = self.max_hp
        self.level = 1

        self.save()

    def __str__(self):
        return f"Hero {self.proto.name} (lvl {self.level}) ({self.hp}/{self.max_hp} hp)"

    @property
    def shield(self):
        value = 0
        for effect in self.get_all_shields():
            value += effect.value
        return value

    def create_modifier(self):
        if self.modifier is not None:
            self.modifier.delete_with_bubbles()
        self.modifier = Stats.create_base()

    def shield_block(self, damage):
        for effect in self.get_all_shields():
            if effect.value > damage:
                effect.value -= damage
                effect.save()
                return 0
            else:
                damage -= effect.value
                effect.value = 0
                effect.delete()
        return damage

    def get_all_shields(self):
        for effect in self.effects.all():
            if isinstance(effect.proto, Shield):
                yield effect

    def get_all_speed_ups(self):
        for effect in self.effects.all():
            if isinstance(effect.proto, SpeedUp):
                yield effect

    def change_hp(self, hp):
        if hp >= 0:
            return self.get_heal(hp)
        else:
            return self.get_damage(-hp)

    def get_damage(self, damage):
        assert damage >= 0
        damage = self.shield_block(damage)

        self.hp -= damage
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
        for effect in self.effects.all():
            if effect.proto.is_live_on_target:
                effect.tick()
        for effect in self.my_effects.all():
            if not effect.proto.is_live_on_target:
                effect.tick()

    def remove_effect(self, effect):
        self.effects.remove(effect)

    def add_effect(self, effect):
        self.effects.add(effect)

    def add_my_effect(self, effect):
        self.my_effects.add(effect)

    @property
    def max_hp(self):
        return self.proto.hp[self.level]

    def start_move(self):
        pass

    @property
    def current_speed(self):
        speed = self.stats.speed.value
        for speed_up in self.get_all_speed_ups():
            speed += speed_up.value
        return speed
