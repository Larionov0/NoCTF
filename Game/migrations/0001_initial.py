# Generated by Django 3.0.3 on 2020-02-24 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceBubble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StatBubble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('next', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prev_price', to='Game.PriceBubble')),
                ('prev', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='next_price', to='Game.PriceBubble')),
            ],
        ),
    ]