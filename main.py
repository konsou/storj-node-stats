import requests
import argparse
from typing import List, Dict

parser = argparse.ArgumentParser(description='Get info about the audits of a Storj node')
parser.add_argument('address', type=str, help='network address of the node')
parser.add_argument('--port', type=int, default=14002, help='port of the node dashboard')
args = parser.parse_args()

NODE_ADDRESS = args.address
PORT = args.port
NODE_FULL_ADDRESS = f"http://{NODE_ADDRESS}:{PORT}"

AUDIT_VETTING_TRESHOLD = 100


def get_satellites() -> List[Dict]:
    r = requests.get(f"{NODE_FULL_ADDRESS}/api/sno")
    return r.json()['satellites']


def get_satellite_info(satellite_id: str) -> Dict:
    r = requests.get(f"{NODE_FULL_ADDRESS}/api/sno/satellite/{satellite_id}")
    return r.json()


if __name__ == '__main__':
    satellites = get_satellites()
    print(f"Stats for {NODE_FULL_ADDRESS}\n")
    for satellite in satellites:
        print(satellite['url'])
        audits = get_satellite_info(satellite['id'])['audit']
        try:
            print(f"Successful audits: {audits['successCount']} ({audits['successCount'] / audits['totalCount'] * 100:.2f} %)")
            if audits['successCount'] > AUDIT_VETTING_TRESHOLD:
                print(f"VETTING COMPLETE!")
            else:
                print(f"Vetting in progress - {audits['successCount'] / AUDIT_VETTING_TRESHOLD * 100:.0f} % complete")
        except ZeroDivisionError:
            print(f"No audits yet")
        print()



