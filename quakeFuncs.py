from urllib.request import *
from json import *
from datetime import *
from operator import *
from utility import *

# GIVEN FUNCTIONS:
# Use these two as-is and do not change them
def get_json(url):
   ''' Function to get a json dictionary from a website.
       url - a string'''
   with urlopen(url) as response:
      html = response.read()
   htmlstr = html.decode("utf-8")
   return loads(htmlstr)

def time_to_str(time):
   ''' Converts integer seconds since epoch to a string.
       time - an int '''
   return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')    
   
# Add Earthquake class definition here   
class Earthquake:

    def __init__(self, place, mag, longitude, latitude, time):
        self.place = place
        self.mag = mag
        self.longitude = longitude
        self.latitude = latitude
        self.time = time

    def __eq__(self, other):
        return self.place == other.place and \
               epsilon_equal(self.mag, other.mag) and \
               epsilon_equal(self.longitude, other.longitude) and \
               epsilon_equal(self.latitude, other.latitude) and \
               self.time == other.time

    def __str__(self):
        return "(%.2f) %40s at %s (%8.3f, %6.3f)" %(self.mag, self.place, time_to_str(self.time), self.longitude, self.latitude)

    def __repr__(self):
        return "%s %s %s %s %s\n"%(self.mag, self.longitude, self.latitude, self.time, self.place)

# Required function - implement me!   
def read_quakes_from_file(filename):
   
    inFile = open(filename, "r")
    earthquakes = []

    for line in inFile:
        
        data = line.split()
        earthquake = Earthquake(' '.join(data[4:]), float(data[0]), float(data[1]), float(data[2]), int(data[3]))
        earthquakes.append(earthquake)

    return earthquakes

# Required function - implement me!
def filter_by_mag(earthquakes, low, high):
    earthquakes = [earthquake for earthquake in earthquakes if earthquake.mag >= low and earthquake.mag <= high]
    return earthquakes
     
# Required function - implement me!
def filter_by_place(earthquakes, word):   
    earthquakes = [earthquake for earthquake in earthquakes if not earthquake.place[1:].lower().find(word.lower()) == -1]
    return earthquakes

# Required function for final part - implement me too!   
def quake_from_feature(feature):
    earthquake = Earthquake(feature["properties"]["place"], feature["properties"]["mag"], feature["geometry"]["coordinates"][0], feature["geometry"]["coordinates"][1], int(feature["properties"]["time"]/1000))
    return earthquake

def sort_by_mag(earthquakes, filename):
    earthquakes.sort(key = attrgetter('mag'), reverse = True)
    newFile = open(filename, 'w')
    for earthquake in earthquakes:
        newFile.write(repr(earthquake))
    return earthquakes

def sort_by_time(earthquakes, filename):
    earthquakes.sort(key = attrgetter('time'), reverse = True)
    newFile = open(filename, 'w')
    for earthquake in earthquakes:
        newFile.write(repr(earthquake))
    return earthquakes

def sort_by_longitude(earthquakes, filename):
    earthquakes.sort(key = attrgetter('longitude'))
    newFile = open(filename, 'w')
    for earthquake in earthquakes:
        newFile.write(repr(earthquake))
    return earthquakes

def sort_by_latitude(earthquakes, filename):
    earthquakes.sort(key = attrgetter('latitude'))
    newFile = open(filename, 'w')
    for earthquake in earthquakes:
        newFile.write(repr(earthquake))
    return earthquakes

def update_quakes(earthquakes, newEarthquakes, filename):
    newFile = open(filename, 'w')
    for earthquake in earthquakes:
        newFile.write(repr(earthquake))
    for earthquake in newEarthquakes:
        newFile.write(repr(earthquake))
    for earthquake in newEarthquakes:
        earthquakes.append(earthquake)
    return earthquakes
