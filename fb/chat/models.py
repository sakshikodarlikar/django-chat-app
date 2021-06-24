from django.contrib.auth.decorators import user_passes_test
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friend_list = models.ManyToManyField(User,blank=True,related_name='friend_list')
    friend_request = models.ManyToManyField(User,blank=True,related_name='friend_request')
    def __str__(self):
        return f"{self.user}"
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Message(models.Model):
    text = models.TextField(max_length=500, blank=True)
    sender = models.ManyToManyField(User,related_name='sender')
    receiver =  models.ManyToManyField(User,related_name='receiver')
    date = models.DateTimeField(default=datetime.now,blank = True)
    def __str__(self):
        return f"{self.text}"