# otuspy-ip2weather
Simply wsgi daemon return weather by ip address

### Installation

copy .deb file from package folder and run

`$ sudo dpkg -i ip2weather-{version}.deb`

Package create his own python virtualenv and his own uwsgi executable.

You may need some python development package, such as `python3-dev`

### Building

Fabfile is developed under python 3.6.

For building new package, just run (under virtualenv):

`$ fab build`

This command create .deb in package folder.

### NOTE

Ip2weather get weather data from `http://api.openweathermap.org`

So, you need create `secrets.py` file with api key, for example:

`WEATHER_API_KEY = 'apikey'`
