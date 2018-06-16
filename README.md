# otuspy-ip2weather
Simply wsgi daemon return weather by ip address

### Installation

copy .deb file from package folder and run

`$ sudo dpkg -i ip2weather-{version}.deb`

Package created his own python virtualenv and his own uwsgi executable.

You may need some python development package, such as `python-dev`

### Building

fabfile is developed under python 3.6
for building new package, just run

`$ fab build`

this command create .deb in package folder

### NOTE

ip2weather get weather data from `http://api.openweathermap.org`
So, you need create `secrets.py` file with api key, for example:
`WEATHER_API_KEY = 'apikey'`
