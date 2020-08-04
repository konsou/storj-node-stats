import requests
from typing import List, Dict

NODE_ADDRESS = 'http://192.168.42.8:14002'


def get_satellites() -> List[Dict]:
    r = requests.get(f"{NODE_ADDRESS}/api/sno")
    return r.json()['satellites']


def get_satellite_info(satellite_id: str) -> Dict:
    r = requests.get(f"{NODE_ADDRESS}/api/sno/satellite/{satellite_id}")
    return r.json()


if __name__ == '__main__':
    satellites = get_satellites()
    for satellite in satellites:
        print(satellite['url'])
        audits = get_satellite_info(satellite['id'])['audit']
        print(f"Successful audits: {audits['successCount']} ({audits['successCount'] / audits['totalCount'] * 100: .2f} %)")
        print()



