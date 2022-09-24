# Project 5 - Earthquakes
#
# Name: Micah Jeffries
# Instructor: Workman

from quakeFuncs import *

def main():

    earthquakes = read_quakes_from_file('quakes.txt')
    choice = 0
    new = False

    while choice != 'q':
        
        print("\n""Earthquakes:""\n""------------")
        
        for earthquake in earthquakes:
            print(earthquake)

        print("\n""Options:""\n""  (s)ort""\n""  (f)ilter""\n""  (n)ew quakes""\n""  (q)uit""\n")
        choice = input("Choice: ")
        choice = choice.lower()
        earthquakes = read_quakes_from_file('quakes.txt')

        if choice == 's':
        
            sort = input("Sort by (m)agnitude, (t)ime, (l)ongitude, or l(a)titude? ")
            sort = sort.lower()

            if sort == 'm':

                earthquakes = sort_by_mag(earthquakes, 'quakes.txt')
                earthquakes = read_quakes_from_file('quakes.txt')

            elif sort == 't':

                earthquakes = sort_by_time(earthquakes, 'quakes.txt')
                earthquakes = read_quakes_from_file('quakes.txt')

            elif sort == 'l':

                earthquakes = sort_by_longitude(earthquakes, 'quakes.txt')
                earthquakes = read_quakes_from_file('quakes.txt')

            elif sort == 'a':

                earthquakes = sort_by_latitude(earthquakes, 'quakes.txt')
                earthquakes = read_quakes_from_file('quakes.txt')

        elif choice == 'f':

            filter = input("Filter by (m)agnitude or (p)lace? ")
            filter = filter.lower()

            if filter == 'm':

                low = float(input("Lower bound: "))
                high = float(input("Upper bound: "))

                earthquakes = filter_by_mag(earthquakes, low, high)

            elif filter == 'p':

                word = input("Search for what string? ")

                earthquakes = filter_by_place(earthquakes, word)

        elif choice == 'n':

            earthquakeData = get_json('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson')
            newEarthquakes = []

            for feature in earthquakeData["features"]:

                earthquake = quake_from_feature(feature)
                if earthquake not in earthquakes:
                    newEarthquakes.append(earthquake)
                    new = True

            earthquakes = update_quakes(earthquakes, newEarthquakes, 'quakes.txt')

            if new:
                print("\n""New quakes found!!!")

            new = False

if __name__ == '__main__':
    main()

