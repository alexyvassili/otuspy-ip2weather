import os
import sys
from fabric.state import env
from fabric.api import local

from settings import PROJECT, PROJECT_DIR, SETTINGS_DIR, LOG_DIR

try:
    from secrets import WEATHER_API_KEY
except ImportError:
    print("Error: variable 'WEATHER_API_KEY' not found in secrets.py")
    sys.exit(1)


def build():
    set_env()
    flush()
    create_folders()
    copy_files()
    flush_permissions()
    create_deb()
    copy_deb_to_project()


def set_env():
    env.PROJECT = PROJECT
    env.VERSION = '0.1'
    env.TMP_DIR = '/tmp'
    env.BUILD_DIR = os.path.join(env.TMP_DIR, env.PROJECT)
    env.BUILD_PROJECT_DIR = env.BUILD_DIR + PROJECT_DIR
    env.BUILD_SETTINGS_DIR = env.BUILD_DIR + SETTINGS_DIR
    env.BUILD_LOG_DIR = env.BUILD_DIR + LOG_DIR
    env.BUILD_NGINX_SITES_AVAILABLE_DIR =  env.BUILD_DIR + '/etc/nginx/sites-available'
    env.BUILD_SYSTEMD_SERVICES_DIR = env.BUILD_DIR + '/etc/systemd/system'


def flush():
    if os.path.exists(env.BUILD_DIR):
        local(f'rm -rf {env.BUILD_DIR}')



def create_folders():
    local(f'mkdir -p {env.BUILD_DIR}')
    local(f'mkdir -p {env.BUILD_PROJECT_DIR}')
    local(f'mkdir -p {env.BUILD_LOG_DIR}')
    local(f'mkdir -p {env.BUILD_SETTINGS_DIR}')
    local(f'mkdir -p {env.BUILD_NGINX_SITES_AVAILABLE_DIR}')
    local(f'mkdir -p {env.BUILD_SYSTEMD_SERVICES_DIR}')
    local(f'mkdir -p {env.BUILD_DIR}/DEBIAN')


def copy_files():
    local(f'cp {env.PROJECT}.py {env.BUILD_PROJECT_DIR}')
    local(f'cp requirements.txt {env.BUILD_PROJECT_DIR}')
    local(f'cp settings.py {env.BUILD_SETTINGS_DIR}')
    local(f'cp secrets.py {env.BUILD_SETTINGS_DIR}')
    local(f'cat secrets.py >> {env.BUILD_SETTINGS_DIR}/settings.py')
    local(f'touch {env.BUILD_LOG_DIR}/{env.PROJECT}.log')
    local(f'cp config/{env.PROJECT}.ini {env.BUILD_SETTINGS_DIR}')
    local(f'cp config/{env.PROJECT}.nginx {env.BUILD_NGINX_SITES_AVAILABLE_DIR}/{env.PROJECT}')
    local(f'cp config/{env.PROJECT}.service {env.BUILD_SYSTEMD_SERVICES_DIR}')
    local(f'cp builddeb/* {env.BUILD_DIR}/DEBIAN')


def flush_permissions():
    local(f'chmod -x {env.BUILD_SETTINGS_DIR}/*')
    local(f'chmod -x {env.BUILD_PROJECT_DIR}/requirements.txt')
    local(f'chmod -x {env.BUILD_NGINX_SITES_AVAILABLE_DIR}/*')
    local(f'chmod -x {env.BUILD_SYSTEMD_SERVICES_DIR}/*')
    local(f'chmod -x {env.BUILD_NGINX_SITES_AVAILABLE_DIR}/*')
    local(f'chmod -x {env.BUILD_DIR}/DEBIAN/conffiles')
    local(f'chmod -x {env.BUILD_DIR}/DEBIAN/control')


def create_deb():
    local(f'cd {env.TMP_DIR}; dpkg -b ./{env.PROJECT} {env.PROJECT}-{env.VERSION}.deb')


def copy_deb_to_project():
    local(f'cp {env.TMP_DIR}/{env.PROJECT}-{env.VERSION}.deb ./package')
