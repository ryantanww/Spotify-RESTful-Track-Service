from rest_framework import serializers
from .models import Tracks

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = '__all__'

class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = ['id', 'track_name', 'artists']