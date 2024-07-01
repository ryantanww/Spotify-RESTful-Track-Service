from django.contrib import admin
from .models import *
# Register your models here.

# Define a custom admin class for the Tracks model 
class TrackAdmin(admin.ModelAdmin):
    # Specify the fields that will be displayed in the admin interface
    list_display = ('track_name', 'artists', 'album', 'genre', 'duration_ms')

# Registers the Tracks model to the custom admin class
admin.site.register(Tracks, TrackAdmin)