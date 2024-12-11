import os
import requests
import xml.etree.ElementTree as ET
import json
import paho.mqtt.client as mqtt
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_and_parse_xml(url):
    response = requests.get(url)
    response.raise_for_status()
    return ET.fromstring(response.content)

def extract_bus_data_without_unit_details(xml_root, base_url):
    buses = []
    for bus in xml_root.findall(".//bus"):
        bus_data = {
            "name": bus.get("name"),
            "type": bus.get("type"),
            "controlmode": bus.get("controlmode"),
            "address": bus.get("address"),
            "port": bus.get("port"),
            "units": []
        }
        for unit in bus.findall("unit"):
            unit_data = {
                "type": unit.get("type"),
                "alarm": unit.get("alarm"),
                "id": unit.get("id"),
                "alias": unit.get("alias"),
                "status": unit.get("status"),
                "name": unit.text
            }
            unit_details_url = f"{base_url}/cgi-bin/mdacxml.cgi?req=devsta&devid={unit.text}"
            unit_details = fetch_and_parse_xml(unit_details_url)
            device = unit_details.find(".//device")
            
            selected_details = {
                "ts": device.find("ts").text if device.find("ts") is not None else None,
                "t1": device.find("t1").text if device.find("t1") is not None else None,
                "run_mode": {subchild.tag: subchild.text for subchild in device.find("run_mode")},
                "fault": {subchild.tag: subchild.text for subchild in device.find("fault")}
            }
            unit_data["details"] = selected_details
            bus_data["units"].append(unit_data)
        buses.append(bus_data)
    return buses

def main():
    base_urls = [
        os.getenv('BASE_URL_1', 'http://10.10.5.56'),
        os.getenv('BASE_URL_2', 'http://10.10.5.55')
    ]
    
    broker = os.getenv('MQTT_BROKER', '172.16.93.83')
    port = int(os.getenv('MQTT_PORT', 1883))
    
    client = mqtt.Client()
    client.connect(broker, port, 60)
    
    while True:
        for base_url in base_urls:
            url = f"{base_url}/cgi-bin/mdacxml.cgi?req=devlist"
            xml_root = fetch_and_parse_xml(url)
            buses = extract_bus_data_without_unit_details(xml_root, base_url)
            
            topic = f"controller/{base_url.split('//')[1].split('/')[0]}"
            message = json.dumps(buses, indent=4)
            
            print(f"Publishing message to topic: {topic}")
            client.publish(topic, message)
            
            time.sleep(15)
    
    client.disconnect()

if __name__ == "__main__":
    main()