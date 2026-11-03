import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL = 300

def check_site(website):
    try:
        response = requests.get(website, timeout=5)

        if 200 <= response.status_code < 300:
            return {"up": True, "status": response.status_code}
        else:
            return {"up": False, "status": response.status_code}

    except requests.exceptions.RequestException:
        return {"up": False, "status": None} 

def get_state(check):
    if check["up"]:
        return "UP"
    else:
        return "DOWN"
    
def log_result(site, check):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = get_state(check)
    
    line = f"{timestamp} | {site} | {state} | {check['status']}\n"

    with open("uptime_log.txt", "a") as file:
        file.write(line)

def send_alert(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(url, data=data, timeout=5)
    except requests.exceptions.RequestException:
        print("⚠️ Could not send Telegram alert")      

def get_code(check):
    if check["status"] is None:
        return "No Response"
    else:
        return check['status']             

def run_checks(chat_id, sites):
    for number, site in enumerate(sites, start=1):
        check = check_site(site)
        log_result(site, check)
        state = get_state(check)
        code = get_code(check)

        if not check["up"]:
            send_alert(chat_id, f"🔴DOWN: {site} ({code})")

        print(f"{number}. {site} - {state} {code}")

def load_sites():
    with open("sites.json", "r") as file:
        data = json.load(file)
        return data          

while True:
    all_sites = load_sites()
    for chat_id, sites in all_sites.items():
        run_checks(chat_id, sites)
    print(f"Waiting {CHECK_INTERVAL} seconds...\n")
    time.sleep(CHECK_INTERVAL)
