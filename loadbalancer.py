import random

import requests
import yaml
from flask import Flask, request

loadbalancer = Flask(__name__)

MANGO_BACKENDS = ['localhost:8081', 'localhost:8082']
APPLE_BACKENDS = ['localhost:9081', 'localhost:9082']

def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

config = load_configuration('loadbalancer.yaml')

@loadbalancer.route('/<path>')
def path_router(path):
    for entry in config['paths']:
        if ('/'+ path) == entry['path']:
            response = requests.get(f'http://{random.choice(entry["servers"])}')
            return response.content, response.status_code
    return 'Not Found', 404

@loadbalancer.route('/')
def router():
    host_header = request.headers['Host']
    if host_header == 'www.mango.com':
        response = requests.get(f'http://{random.choice(MANGO_BACKENDS)}')
        return response.content, response.status_code
    elif host_header == 'www.apple.com':
        response = requests.get(f'http://{random.choice(APPLE_BACKENDS)}')
        return response.content, response.status_code
    else:
        return 'Not Found', 404