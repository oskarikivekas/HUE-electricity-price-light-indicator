## The hue module provides basic interface to interact with bridge and connected lights.
## During development, use env to disable SSL verification for ease of use 
## API key and bridge IP can be obtained from https://discovery.meethue.com. This should be automated later, once I figure the actual usecase

import requests
import json
import os

# for development
ssl_disabled = os.environ.get('SSL_DISABLE', 'True').lower() == 'true'

# TODO: create separate file for commonly used payloads


class HueBridge:

    def __init__(self, bridge_ip, api_key):
        self.BASE_API = f"https://{bridge_ip}/clip/v2"
        self.API_KEY = api_key
        self.RESOURCES = f"{self.BASE_API}/resource"

    # TODO: add error handling

    def discover_lights(self):
        lights = []
        endpoint = f"{self.RESOURCES}/light"

        headers = {
            'hue-application-key': self.API_KEY
        }

        res = requests.get(endpoint, headers=headers, verify=not ssl_disabled)
        json_data = res.json()
        for light in json_data["data"]:
            light_id = light["id"]
            light_name = light["metadata"]["name"]
            lights.append((light_id, light_name))
        return lights

    def turn_on_light(self, light_id):

        endpoint = f"{self.RESOURCES}/light/{light_id}"
        data = {
            "on": {
                "on": True
            }
        }
        headers = {
            'hue-application-key': self.API_KEY,
            'content-type': "application/json"
        }
        response = requests.put(endpoint, json=data,
                                headers=headers, verify=not ssl_disabled)
        if response.status_code == 200:
            return True
        else:
            return False

    def turn_off_light(self, light_id):

        endpoint = f"{self.RESOURCES}/light/{light_id}"

        data = {
            "on": {
                "on": False
            }
        }
        headers = {
            'hue-application-key': self.API_KEY,
            'content-type': "application/json"
        }
        response = requests.put(endpoint, json=data,
                                headers=headers, verify=not ssl_disabled)

        if response.status_code == 200:
            return True
        else:
            return False


# maybe a bit inverse relationship but it works. Each light obtains its bridge so its easier to 
# control lights independently. Not really necessary for this usecase though..

class HueLight:
    def __init__(self, light_id, light_name, bridge):
        self.light_id = light_id
        self.name = light_name
        self.bridge = bridge

    def get_bridge_info(self):
        return self.bridge

    def turn_on(self):
        if self.bridge:
            return self.bridge.turn_on_light(self.light_id)

    def turn_off(self):
        if self.bridge:
            return self.bridge.turn_off_light(self.light_id)

    #
    def set_multiple_light_options(self, brightness=None, color=None,color_temperature=None):
        
