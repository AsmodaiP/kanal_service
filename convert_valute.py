

import xml.etree.ElementTree as ET

URL = 'https://www.cbr.ru/scripts/XML_daily.asp'


def get_xml() -> ET.Element:
    import requests
    response = requests.get(URL)
    return ET.fromstring(response.text)


def find_valute(xml: ET.Element, code: str) -> ET.Element:
    return xml.find(f'.//Valute[@ID="{code}"]')


def get_course(code: str) -> float:
    xml = get_xml()
    valute = find_valute(xml, code)
    return float(valute.find('Value').text.replace(',', '.'))