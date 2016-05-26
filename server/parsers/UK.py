import arrow
import requests
import xml.etree.ElementTree as ET

COUNTRY_CODE = 'UK'

def fetch_UK():
    url = 'http://www.bmreports.com/bsp/additional/soapfunctions.php?element=generationbyfueltypetable'

    response = requests.get(url)
    root = ET.fromstring(response.content)
    data = root[0]

    parsed = {}
    for item in data:
        parsed[item.get('TYPE')] = float(item.get('VAL'))

    obj = {
        'countryCode': COUNTRY_CODE,
        'datetime': arrow.get(arrow.get(data.get('AT')).datetime, 
            'Europe/London').datetime
    }
    obj['consumption'] = {}
    obj['production'] = {
        'coal': parsed['COAL'],
        'gas': parsed['CCGT'] + parsed['OCGT'],
        'nuclear': parsed['NUCLEAR'],
        'wind': parsed['WIND'],
        'oil': parsed['OIL'],
        'hydro': parsed['PS'] + parsed['NPSHYD'],
        'other': parsed['OTHER']
    }
    obj['imports'] = {
        'FR': parsed['INTFR'],
        'IE': parsed['INTIRL'],
        'NL': parsed['INTNED']
    }
    obj['co2'] = (
        parsed['CCGT'] * 360 +
        parsed['OCGT'] * 480 +
        parsed['COAL'] * 910 +
        parsed['OTHER'] * 300 +
        parsed['OIL'] * 610 +
        parsed['INTFR'] * 90 +
        parsed['INTIRL'] * 450 +
        parsed['INTNED'] * 550 +
        parsed['INTEW'] * 450)/0.93

    return obj
