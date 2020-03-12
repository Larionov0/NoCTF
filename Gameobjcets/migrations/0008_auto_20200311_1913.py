# Generated by Django 3.0.3 on 2020-03-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gameobjcets', '0007_remove_hero_shield'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='my_effects',
            field=models.ManyToManyField(blank=True, related_name='maker', to='Gameobjcets.Effect'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='effects',
            field=models.ManyToManyField(blank=True, to='Gameobjcets.Effect'),
        ),
    ]
