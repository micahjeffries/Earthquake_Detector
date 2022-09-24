import unittest
from quakeFuncs import *

class TestCases(unittest.TestCase):
          
   def test_earthquake_init(self):
      quake = Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290)
      self.assertEqual(quake.place, '12km SSW of Idyllwild, CA')
      self.assertAlmostEqual(quake.mag, 0.97)
      self.assertAlmostEqual(quake.longitude, -116.7551651)
      self.assertAlmostEqual(quake.latitude, 33.6391678)
      self.assertEqual(quake.time, 1488177290)  

   def test_earthquakes_equal_0(self):   
      quake1 = Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290)  
      quake2 = Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290)  
      self.assertEqual(quake1, quake2)

   def test_earthquakes_equal_1(self):   
      quake1 = Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290)  
      quake2 = Earthquake('13km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290)  
      self.assertNotEqual(quake1, quake2)

   def test_read_file_0(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290))
      quakes.append(Earthquake('5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002, 1488173538))
      # call read_file with 'test0.txt'
      self.assertEqual(read_quakes_from_file('test0.txt'), quakes)

   def test_filter_by_mag_0(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678, 1488177290))
      quakes.append(Earthquake('5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002, 1488173538))
      quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
      filtered = []
      filtered.append(Earthquake('5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002, 1488173538))
      filtered.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
      self.assertEqual(filter_by_mag(quakes, 1, 3), filtered)

   def test_filter_by_mag_1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      filtered = []
      filtered.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      self.assertEqual(filter_by_mag(quakes, 1, 3), filtered)

   def test_filter_by_place_0(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
      quakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
      quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
      filtered = []
      filtered.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
      filtered.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
      self.assertEqual(filter_by_place(quakes, "ca"), filtered)

   def test_filter_by_place_1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      filtered = []
      filtered.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      filtered.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      filtered.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      self.assertEqual(filter_by_place(quakes, "ca"), filtered)

  # Use this test when ready to work on the json data. 
   def test_quake_from_feature(self):
      feature = {
            "geometry": {
                "coordinates": [
                    -117.4906667,
                    33.9131667,
                    0.25
                ],
                "type": "Point"
            },
            "id": "ci37814000",
            "properties": {
                "code": "37814000",
                "detail": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ci37814000.geojson",
                "dmin": 0.2836,
                "gap": 87,
                "ids": ",ci37814000,",
                "mag": 1.24,
                "magType": "ml",
                "net": "ci",
                "nst": 8,
                "place": "5km NE of Home Gardens, CA",
                "rms": 0.27,
                "sig": 24,
                "sources": ",ci,",
                "status": "automatic",
                "time": 1488179250520,
                "title": "M 1.2 - 5km NE of Home Gardens, CA",
                "tsunami": 0,
                "type": "earthquake",
                "types": ",geoserve,nearby-cities,origin,phase-data,scitech-link,",
                "tz": -480,
                "updated": 1488179487273,
                "url": "http://earthquake.usgs.gov/earthquakes/eventpage/ci37814000"
            },
            "type": "Feature"
        }
      quake1 = quake_from_feature(feature)
      quake2 = Earthquake("5km NE of Home Gardens, CA", 1.24, -117.4906667, 33.9131667, 1488179250)
      self.assertEqual(quake1, quake2)


   def test_sort_by_mag0(self):
        quakes = []
        quakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        quakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted = []
        sorted.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        sorted.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        self.assertEqual(sort_by_mag(quakes,'earthquakes.txt'), sorted)

   def test_sort_by_mag1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted = []
      sorted.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      sorted.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      self.assertEqual(sort_by_mag(quakes, 'earthquakes.txt'), sorted)

   def test_sort_by_time0(self):
        quakes = []
        quakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        quakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted = []
        sorted.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        sorted.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        self.assertEqual(sort_by_time(quakes,'earthquakes.txt'), sorted)

   def test_sort_by_time1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted = []
      sorted.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      sorted.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      self.assertEqual(sort_by_time(quakes, 'earthquakes.txt'), sorted)

   def test_sort_by_longitude0(self):
        quakes = []
        quakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        quakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted = []
        sorted.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        sorted.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        self.assertEqual(sort_by_longitude(quakes,'earthquakes.txt'), sorted)

   def test_sort_by_longitude1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted = []
      sorted.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      sorted.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      sorted.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      self.assertEqual(sort_by_longitude(quakes, 'earthquakes.txt'), sorted)

   def test_sort_by_latitude0(self):
        quakes = []
        quakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        quakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        quakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        sorted = []
        sorted.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        sorted.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        sorted.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        self.assertEqual(sort_by_latitude(quakes,'earthquakes.txt'), sorted)

   def test_sort_by_latitude1(self):
      quakes = []
      quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      sorted = []
      sorted.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
      sorted.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
      sorted.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
      self.assertEqual(sort_by_latitude(quakes, 'earthquakes.txt'), sorted)

   def test_update_quakes(self):
        quakes = []
        quakes.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
        quakes.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
        quakes.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
        newQuakes = []
        newQuakes.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        newQuakes.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        newQuakes.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        updated = []
        updated.append(Earthquake('12km SSW of Los Angeles, CA', 9.8, -100.5, 33.0, 1488177301))
        updated.append(Earthquake('5km S of Auburn, California', 0.11, -121.5, 26.7, 1488173302))
        updated.append(Earthquake('100km SE of San Francisco, CA', 1.9, 123.3, 58.1, 1488219303))
        updated.append(Earthquake('12km SSW of Idyllwild, ca', 0.97, -116.7551651, 33.6391678, 1488177290))
        updated.append(Earthquake('5km S of Gilroy, california', 2.19, -121.5801697, 36.9580002, 1488173538))
        updated.append(Earthquake('100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548, 1488219604))
        self.assertEqual(update_quakes(quakes, newQuakes, 'earthquakes.txt'), updated)

# Run the unit tests.
if __name__ == '__main__':
   unittest.main()

