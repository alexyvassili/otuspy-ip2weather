import os

PROJECT = "ip2weather"

PROJECT_DIR = "/usr/local/{PROJECT}".format(PROJECT=PROJECT)
LOG_DIR = "/var/log/{PROJECT}/".format(PROJECT=PROJECT)
SETTINGS_DIR = "/usr/local/etc/{PROJECT}/".format(PROJECT=PROJECT)

STATUS_OK = '200 OK'
STATUS_ERROR = '400'

MAX_RETRIES = os.environ.get("MAX_RETRIES", 5)

IP_INFO_URL = "https://ipinfo.io/{ip}"

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
