#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2020-2024 Erriez
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Example Python script to send a button press or read power status.
"""

import json
import requests
import time


# https://developers.home-assistant.io/docs/api/rest/
HA_SERVER = 'http://yourserver:8123'
HA_TOKEN = 'YOUR_TOKEN'
VERBOSE = True


def print_json(json_obj):
    print(json.dumps(json_obj, indent=2))


def ha_get(endpoint):
    url = '{}/{}'.format(HA_SERVER, endpoint)
    headers = {
        'Authorization': 'Bearer {}'.format(HA_TOKEN),
        'content-type': 'application/json',
    }

    if VERBOSE:
        print('GET: {}'.format(url))
        print(headers)

    return requests.get(url, headers=headers)


def ha_post(endpoint, data):
    url = '{}/{}'.format(HA_SERVER, endpoint)
    headers = {
        'Authorization': 'Bearer {}'.format(HA_TOKEN),
        'content-type': 'application/json',
    }

    if VERBOSE:
        print('POST: {}'.format(url))
        print(headers)
        print(data)

    return requests.post(url, headers=headers, data=data)


# ------------------------------------------------------------------------------------
def ha_get_config():
    return json.loads(ha_get('api/config').text)


def ha_get_state(entity_id):
    r = ha_get('api/states/{}'.format(entity_id))
    r_text = json.loads(r.text)
    if VERBOSE:
        print('Received code: {}'.format(r.status_code))
        print_json(r_text)
    return r_text.get('state')


def ha_post_state(entity_id, state):
    return ha_post('api/states/{}'.format(entity_id), '{ "state": "%s" }' % state)


def ha_post_switch(entity_id):
    return ha_post('api/services/switch/turn_on', '{ "entity_id": "%s" }' % entity_id)


# ------------------------------------------------------------------------------------
def post_nas_power_button_press():
    return ha_post_switch('switch.nas_power_button')


def get_nas_power_state():
    return ha_get_state('binary_sensor.nas_power_sense')


# ------------------------------------------------------------------------------------
def post_bell_button_press():
    return ha_post_switch('switch.bell')


def get_bell_state():
    return ha_post_switch('switch.bell')


# ------------------------------------------------------------------------------------
if __name__ == '__main__':
    print_json(ha_get_config())

    #print(post_bell_button_press())

    print(post_nas_power_button_press())
    time.sleep(1)
    print('NAS power state: {}'.format(get_nas_power_state()))
