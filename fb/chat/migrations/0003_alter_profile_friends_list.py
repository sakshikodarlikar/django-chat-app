# Generated by Django 3.2.4 on 2021-06-14 10:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_profile_friends_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends_list',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
