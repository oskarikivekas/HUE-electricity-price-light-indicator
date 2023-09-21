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
        
    def set_light_with_payload(self, light_id, payload):
        endpoint = f"{self.RESOURCES}/light/{light_id}"
        headers = {
            'hue-application-key': self.API_KEY,
            'content-type': "application/json"
        }
        response = requests.put(endpoint, json=payload,
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


    def set_multiple_light_options(self, brightness=0, color=None, color_temperature=0):
        
        data = {
            "dimming": {
                "brightness": brightness
                },
            "color": {
                "xy": {"x":color[0], "y":color[1]}
                }
            }
            # "color_temperature": {
            #     "mirek": {color_temperature}
            #     }
        return self.bridge.set_light_with_payload(self.light_id, data) 
    
    def set_color_match_price(self, electricity_price):
        if electricity_price <= 0.05:
            print(f"Price is : {electricity_price}€, light is set to: Light blue")
            return self.set_multiple_light_options(brightness=80, color=[0.16, 0.06])
        elif 0.06 <= electricity_price <= 0.10:
            print(f"Price is : {electricity_price}€, light is set to:  Green")
            return self.set_multiple_light_options(brightness=80, color=[0.214, 0.709])
        elif 0.11 <= electricity_price <= 0.15:
            print(f"Price is : {electricity_price}€, light is set to: Light green")
            return self.set_multiple_light_options(brightness=80, color=[0.299, 0.588])
        elif 0.16 <= electricity_price <= 0.20:
            print(f"Price is : {electricity_price}€, light is set to: Yellow")
            return self.set_multiple_light_options(brightness=80, color=[0.567, 0.431])
        elif 0.21 <= electricity_price <= 0.25:
            print(f"Price is : {electricity_price}€, light is set to: Orange")
            return self.set_multiple_light_options(brightness=80, color=[0.569, 0.414])
        elif 0.26 <= electricity_price <= 0.35:
            print(f"Price is : {electricity_price}€, light is set to: Light red")
            return self.set_multiple_light_options(brightness=80, color=[0.675, 0.322])
        else:
            print(f"Price is : {electricity_price}€, light is set to: Really red")
            return self.set_multiple_light_options(brightness=80, color=[0.698, 0.31])
    