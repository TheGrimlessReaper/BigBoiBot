# BigBoiBot
Just a fun lil bot. Features include: sending reminders, which are backed up in a JSON file, sending the weather (in the US), and other dumb stuff.

##  Extra Files
For Big Boi Bot to run, you need to put the proper info into a configu.txt file in the same directory as the Python script file (sample file provided), put your bot token in a token.txt file in the same directory as the Python script file, and likewise with the Google Maps API Key in a mapskey.txt file. Also needs an empty reminders.json file. Replace the paths where Python reads the txt and json files with your own.

## Discord.py
Made using [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html). ([Github](https://github.com/Rapptz/discord.py))

## Weather.gov API
Weather provided by the [weather.gov API](https://www.weather.gov/documentation/services-web-api).
Using [this wrapper](https://github.com/paulokuong/noaa).

## Google Maps API
Geocoding provided by [Google Maps API](https://cloud.google.com/maps-platform/#get-started).
Using [this wrapper](https://github.com/googlemaps/google-maps-services-python).
