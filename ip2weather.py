import sys
import os
import logging

sys.path.append('/usr/local/etc/ip2weather')

import requests
import json
import socket
import time

from settings import STATUS_OK, STATUS_ERROR, MAX_RETRIES, IP_INFO_URL, WEATHER_URL, LOG_DIR

try:
    from settings import WEATHER_API_KEY
except ImportError:
    from secrets import WEATHER_API_KEY

LOGGING_FORMAT = '[%(asctime)s] %(levelname).1s %(message)s'
LOGGING_LEVEL = logging.INFO
LOGGING_FILE = os.path.join(LOG_DIR, 'ip2weather.log')
logging.basicConfig(format=LOGGING_FORMAT, datefmt='%Y.%m.%d %H:%M:%S', level=LOGGING_LEVEL,
                            filename=LOGGING_FILE)

def get(url, params=None, timeout=5, backoff_factor=0.3):
    if not params:
        params = dict()
    for n in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException:
            if n == MAX_RETRIES - 1:
                raise
            backoff_value = backoff_factor * (2 ** n)
            time.sleep(backoff_value)


def get_ip_info(ip):
    url = IP_INFO_URL.format(ip=ip)
    response = get(url)
    return response.json()


def get_weather(lat, lon):
    url = WEATHER_URL
    response = get(url, params={
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "APPID": WEATHER_API_KEY
    })
    return response.json()


def is_valid(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def get_request_ip(uri):
    ip = uri.split('/')[-1]
    return ip


def get_request_uri(env):
    uri = env.get("REQUEST_URI", "")
    return uri


def get_response(env):
    uri = get_request_uri(env)
    ip = get_request_ip(uri)

    if not is_valid(ip):
        return STATUS_ERROR, json.dumps({"error": "Invalid IP address"})

    if not WEATHER_API_KEY:
        return STATUS_ERROR, json.dumps({"error": "NO WEATHER_APPID"})

    try:
        ip_info = get_ip_info(ip)
        lat, lon = ip_info["loc"].split(",")
        weather_data = get_weather(lat, lon)
    except requests.exceptions.RequestException as err:
        return err.response.status_code, json.dumps({"error": err.args[0]})
    except ValueError as err:
        return STATUS_ERROR, json.dumps({"error": err.args[0]})

    city = weather_data["name"]
    temp = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]

    return STATUS_OK, json.dumps({
        "city": city,
        "temp": temp,
        "conditions": description
    })


def application(env, start_response):
    uri = get_request_uri(env)
    status, response_body = get_response(env)

    if '200' in status:
        logging.info("Request URI: {uri} -- Status: {status}, Response length: {length}".format(
            uri=uri,
            status=status,
            length=len(response_body)

        ))
    else:
        logging.warning("Request URI: {uri} -- Status: {status}, Response: {response_body}".format(
            uri=uri,
            status=status,
            response_body=response_body
        ))

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]
