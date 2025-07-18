# Generated by Django 5.2.4 on 2025-07-04 14:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendezvous', '0005_temoignage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='temoignage',
            name='auteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='temoignage',
            name='reponse_coach',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='temoignage',
            name='signalement',
            field=models.BooleanField(default=False),
        ),
    ]
