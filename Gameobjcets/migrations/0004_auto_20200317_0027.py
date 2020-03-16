# Generated by Django 3.0.3 on 2020-03-16 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Gameobjcets', '0003_auto_20200317_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='distance_on_this_move',
        ),
        migrations.AddField(
            model_name='hero',
            name='energy_on_this_move',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='hero',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Gameobjcets.Team'),
        ),
    ]
