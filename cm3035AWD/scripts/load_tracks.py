import os
import sys
import django
import csv
from tracks.models import Tracks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
sys.path.append("C:/Users/hu1Dr/git_repository/CM3035-Advanced-Web-Development/cm3035AWD")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm3035AWD.settings')
django.setup()

data_file = 'scripts/updated_track_data.csv'

# Clear existing data
Tracks.objects.all().delete()

try:
    with open(data_file, encoding='utf-8-sig') as csv_file:  # specify encoding
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)  # Skip header
        count = 0
        for row in csv_reader:
            count += 1
            try:
                # Create track
                track = Tracks.objects.create(
                    track_name=row[2],
                    artists=row[0],
                    album=row[1],
                    genre=row[18],
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
            except Exception as e:
                print(f"Error loading track at row {count}: {str(e)}")
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: File '{data_file}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")