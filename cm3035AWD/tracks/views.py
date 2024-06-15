from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.views.generic.edit import CreateView

class TrackCreate(CreateView):
    model = Tracks
    template_name = 'tracks/create_track.html'
    form_class = TrackForm
    success_url = "/api/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Tracks.objects.all()
        return context