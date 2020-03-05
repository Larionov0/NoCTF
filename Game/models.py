from django.db import models


class PriceBubble(models.Model):
    price = models.IntegerField(default=0)


class StatBubble(models.Model):
    value = models.IntegerField(default=0)
    next = models.OneToOneField(PriceBubble, on_delete=models.CASCADE, null=True, blank=True, related_name='prev_stat')
    prev = models.OneToOneField(PriceBubble, on_delete=models.CASCADE, null=True, blank=True, related_name='next_stat')
