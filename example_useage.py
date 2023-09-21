import os
import time
import json
from modules import hue
from modules import electricity_price_api

ssl_disabled = os.environ.get('SSL_DISABLE', 'True').lower() == 'true'

def main():
    bridge_ip = None
    api_key = None
    
    #Load config and parse ip + apikey
    with open('config/hue_config.json', 'r') as config_file:
        config_data = json.load(config_file)
        print("Hue config loaded")
        
        for secret in config_data.get('secrets', []):
            if 'hue-application-key' in secret:
                api_key = secret['hue-application-key']
            elif 'bridge-ip' in secret:
                bridge_ip = secret['jkaari-bridge-ip']
    

    if bridge_ip and api_key:
        
        bridge = hue.HueBridge(bridge_ip, api_key)
        lights = bridge.discover_lights()
        
        # example
        for light in lights:
            if light[1] == 'Yöpöytä':
                light_id, light_name =light[0], light[1]
                
        nightstand_light = hue.HueLight(light_id=light_id, light_name=light_name, bridge=bridge)
        
        while True:
            price = electricity_price_api.get_electricity_price_just_now()
            nightstand_light.turn_on()
            nightstand_light.set_color_match_price(price)
            # Refresh every 5 minutes
            time.sleep(300)


if __name__=="__main__":
    main()