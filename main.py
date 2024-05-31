import requests
import json
import time
from httplib2 import Http

## API endpoints for polygon heimdall
CP_LATEST_URL = 'https://heimdall-api.polygon.technology/checkpoints/latest'
OVERVIEW_URL = 'https://heimdall-api.polygon.technology/overview'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

NOTIFICATION_URL = <gchat-webhook-url>  # Add gchat webhook url here
NOTIFICATION_HEADERS = {"Content-Type": "application/json; charset=UTF-8"}

# Function to send notification to gchat channel when triggered
def notification(message):
    """Google Chat incoming webhook quickstart."""
    app_message = {"text": message}
    http_obj = Http()
    response = http_obj.request(
        uri=NOTIFICATION_URL,
        method="POST",
        headers=NOTIFICATION_HEADERS,
        body=json.dumps(app_message),
    )

# Check if validator with ID 12 and 16, signed or missed latest checkpoint
def valSign(cp_number):
    overview_resp = requests.get(OVERVIEW_URL, headers=HEADERS).json()
    validators = overview_resp["result"]["validator_set"]["validators"]
    id_12_present = any(validator["ID"] == 12 for validator in validators)
    id_16_present = any(validator["ID"] == 16 for validator in validators)
    
    if not id_12_present:
        notification(f"Worldpay missed the checkpoint: {cp_number}")
    # else:
    #     notification(f"Worldpay signed the checkpoint: {cp_number}")
    
    if not id_16_present:
        notification(f"BCW Technologies missed the checkpoint: {cp_number}")
    # else:
    #     notification(f"BCW Technologies signed the checkpoint: {cp_number}")

if __name__ == '__main__':
    session = requests.Session()
    cp_latest_resp = session.get(CP_LATEST_URL, headers=HEADERS).json()
    previous_cp = cp_latest_resp["result"]["id"]

    while True:
        cp_latest_resp = session.get(CP_LATEST_URL, headers=HEADERS).json()
        latest_cp = cp_latest_resp["result"]["id"]
        if previous_cp != latest_cp:
            previous_cp = latest_cp
            valSign(latest_cp)
        time.sleep(60)
