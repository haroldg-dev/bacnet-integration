import os
import requests
import xml.etree.ElementTree as ET
import json
from dotenv import load_dotenv

load_dotenv()

def fetch_and_parse_xml(url):
    response = requests.get(url)
    response.raise_for_status()
    return ET.fromstring(response.content)

def extract_bus_data(xml_root, base_url):
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
            unit_data["details"] = extract_unit_details(unit_details)
            bus_data["units"].append(unit_data)
        buses.append(bus_data)
    return buses

def extract_unit_details(xml_root):
    details = {}
    for child in xml_root.find(".//device"):
        if list(child):
            details[child.tag] = {subchild.tag: subchild.text for subchild in child}
        else:
            details[child.tag] = child.text
    return details

def main():
    base_urls = [
        os.getenv('BASE_URL_1', 'http://10.10.5.56'),
        os.getenv('BASE_URL_2', 'http://10.10.5.55')
    ]
    
    all_buses = []
    for base_url in base_urls:
        url = f"{base_url}/cgi-bin/mdacxml.cgi?req=devlist"
        xml_root = fetch_and_parse_xml(url)
        buses = extract_bus_data(xml_root, base_url)
        all_buses.extend(buses)
    
    json_data = json.dumps(all_buses, indent=4)
    with open('output.json', 'w') as f:
        f.write(json_data)

if __name__ == "__main__":
    main()