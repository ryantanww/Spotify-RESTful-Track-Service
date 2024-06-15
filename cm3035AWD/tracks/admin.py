from django.contrib import admin
from .models import *
# Register your models here.
class TrackAdmin(admin.ModelAdmin):
    list_display = ('track_name', 'artists', 'album', 'genre', 'popularity', 'duration_ms', 'explicit')

admin.site.register(Tracks, TrackAdmin)