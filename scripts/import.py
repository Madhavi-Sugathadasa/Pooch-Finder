import csv
from pooch_finder.models import Location
from django.conf import settings


def run():
    #f = open(getattr(settings, "BASE_DIR", None) + "/australian_postcodes.csv")
    with open(getattr(settings, "BASE_DIR", None) + "/australian_postcodes.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location = Location()
            location.postcode = row['postcode']
            location.suburb = row['locality']
            location.state = row['state']
            location.lon = row['long']
            location.lat = row['lat']
            location.save() 
            print(location.postcode + " added")
    #f.close() 
