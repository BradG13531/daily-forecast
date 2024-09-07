import requests
from bs4 import BeautifulSoup
import json
import csv
import sys

degrees = "\N{DEGREE SIGN}F"

try:
    lines = []
    userInfo = open("city-information.txt")
    lines = userInfo.readlines()
    userInfo.close
    
    if len(lines) == 0:
        print("'city-information.txt' is empty, make sure to have the file located in the 'Daily-forecast' parent folder with the correct format found in the README.md.")
        sys.exit()

except (IOError, OSError):
    print("Could not open/read the 'city-information.txt' file, make sure that the file is located in the 'Daily-Forecast' parent folder.")
    sys.exit()

country = lines[0][8:].strip().title()
state = lines[1][6:].strip().title()
city = lines[2][5:].strip().title()

try:
    cityDB = csv.reader(open("worldcities.csv", "r", encoding="utf8"), delimiter=",")

except (IOError, OSError):
    print("Could not open/read the 'worldcities.csv' file, make sure that the file is located in the 'Daily-Forecast' parent folder.")
    sys.exit()

lat = None
lng = None
for row in cityDB:
    if city == row[1] and state == row[7] and country == row[4]:
        lat = row[2]
        lng = row[3]

if lat is None and lng is None:
    print("Location not found.\nMake sure that your entered location can be found in 'worldcities.csv'.")

# The url to scrape
url = f"https://api.weather.gov/points/{lat},{lng}"

# Stores the request and converts it to json
# This data will let us convert the lat and lng to grid coordinates
response = requests.get(url)
parsedRequest = response.json()

# The Weather stations call will find the closest weather station and grab the current temperature
weatherStations = requests.get(parsedRequest["properties"]["observationStations"])
parsedStations = weatherStations.json()

closestStation = requests.get(parsedStations["features"][0]["id"] + "/observations")
parsedClosestStation = closestStation.json()

currentTemp = round(parsedClosestStation["features"][0]["properties"]["temperature"]["value"] * 9/5 + 32)

print(f"The current temperature is: {currentTemp}{degrees}")

# The forecast call will give us forecasts for several 12 hour periods in the future
forecastResponse = requests.get(parsedRequest["properties"]["forecast"])
parsedForecast = forecastResponse.json()

print(f"The weather {parsedForecast["properties"]["periods"][0]["name"].lower()} will be: {parsedForecast["properties"]["periods"][0]["temperature"]}{degrees}")

# # Create soup object with the type of parser (html) and the content to be parsed
# soup = BeautifulSoup(response.content, 'html.parser')
