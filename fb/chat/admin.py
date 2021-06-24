from django.contrib import admin

from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location','birth_date','bio')


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Message)
