import os
import sys
import django
import csv

sys.path.append("C:\Users\hu1Dr\git_repository\CM3035-Advanced-Web-Development\cm3035AWD")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm3035AWD.settings')
django.setup()

from tracks.models import Track, Artist, Album, Genre

data_file = 'updated_track_data.csv'

# Clear existing data
Track.objects.all().delete()
Artist.objects.all().delete()
Album.objects.all().delete()
Genre.objects.all().delete()

artists_cache = {}

with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)  # Skip header
    for row in csv_reader:
        # Splitting multiple artists
        artist_names = row[0].split(';')
        # Check if artists are already created or create new ones
        artists = [artists_cache.get(name, Artist.objects.create(name=name)) for name in artist_names]

        # Create album if not exists
        album, created = Album.objects.get_or_create(name=row[1])

        # Create genre if not exists
        genre, created = Genre.objects.get_or_create(name=row[18])

        # Create track
        track = Track.objects.create(
            track_name=row[2],
            album=album,
            genre=genre,
            popularity=int(row[3]),
            duration_ms=int(row[4]),
            explicit=row[5] == 'True',
            danceability=float(row[6]),
            energy=float(row[7]),
            key=int(row[8]),
            loudness=float(row[9]),
            mode=int(row[10]),
            speechiness=float(row[11]),
            acousticness=float(row[12]),
            instrumentalness=float(row[13]),
            liveness=float(row[14]),
            valence=float(row[15]),
            tempo=float(row[16]),
            time_signature=int(row[17]),
        )
        # Add artists to the track
        track.artists.add(*artists)

        # Update cache with newly created artists
        for artist in artists:
            artists_cache[artist.name] = artist

print("Data loaded successfully.")
