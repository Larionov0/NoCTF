# Generated by Django 3.0.3 on 2020-03-07 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statbubble',
            name='next',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_stat', to='Game.PriceBubble'),
        ),
        migrations.AlterField(
            model_name='statbubble',
            name='prev',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_stat', to='Game.PriceBubble'),
        ),
    ]