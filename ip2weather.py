import requests
import json
import socket
import time

from settings import STATUS_OK, STATUS_ERROR, MAX_RETRIES, IP_INFO_URL, WEATHER_URL
from secrets import WEATHER_API_KEY


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


def get_request_ip(env):
    uri = env.get("REQUEST_URI", "")
    ip = uri.split('/')[-1]
    return ip


def get_response(env):
    ip = get_request_ip(env)
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
    status, response_body = get_response(env)
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]


print(
    get_response({
        # 'REQUEST_URI': 'http://localhost/ip2w/176.14.221.123',
        'REQUEST_URI': 'http://localhost/ip2w/195.208.131.1',
    })
)

