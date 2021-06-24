# Generated by Django 3.2.4 on 2021-06-24 18:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0006_message_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ManyToManyField(related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ManyToManyField(related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]