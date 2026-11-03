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

def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        if not response.ok:
            print("⚠️ Telegram error:", response.json().get("description"))
    except requests.exceptions.RequestException:
        print("⚠️ Could not send Telegram message")    

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
            send_message(chat_id, f"🔴DOWN: {site} ({code})")

        print(f"{number}. {site} - {state} {code}")

def load_sites():
    with open("sites.json", "r") as file:
        data = json.load(file)
        return data      

def save_sites(all_sites):
    with open("sites.json", "w") as file:
        json.dump(all_sites, file, indent=2)      

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url, params={"offset": offset}, timeout=10)
        return response.json()["result"]
    except requests.exceptions.RequestException:
        print("⚠️ Could not get Telegram messages")
        return []  

def handle_message(chat_id, text):
    parts = text.split()
    if not parts:
        return
    command = parts[0]

    if command == "/list":
        all_sites = load_sites()
        sites = all_sites.get(str(chat_id), [])

        if not sites:
            send_message(chat_id, "You have no sites yet.")
            return

        reply = "Your monitored sites:\n"
        for number, site in enumerate(sites, start=1):
            reply += f"{number}. {site}\n"

        send_message(chat_id, reply)

    elif command == "/add":
        if len(parts) < 2:
            send_message(chat_id, "Usage: /add https://example.com")
            return
        url = parts[1]

        if not (url.startswith("http://") or url.startswith("https://")):
            send_message(chat_id, "❌ The URL must start with http:// or https://")
            return

        all_sites = load_sites()
        key = str(chat_id)
        sites = all_sites.get(key, [])

        if url in sites:
            send_message(chat_id, "❌ That site is already in your list")
            return

        if len(sites) >= 10:
            send_message(chat_id, "❌ You can monitor up to 10 sites")
            return

        sites.append(url)
        all_sites[key] = sites
        save_sites(all_sites)
        send_message(chat_id, f"✅ Added {url}")

    elif command == "/remove":
        if len(parts) < 2 or not parts[1].isdigit():
            send_message(chat_id, "Usage: /remove 2  (use the number from /list)")
            return
        number = int(parts[1])

        all_sites = load_sites()
        key = str(chat_id)
        sites = all_sites.get(key, [])

        if number < 1 or number > len(sites):
            send_message(chat_id, "❌ No site with that number. Send /list to see your sites.")
            return

        removed = sites.pop(number - 1)
        all_sites[key] = sites
        save_sites(all_sites)
        send_message(chat_id, f"🗑️ Removed {removed}")    

offset = None
last_check = 0

while True:
    for update in get_updates(offset):
        offset = update["update_id"] + 1
        message = update.get("message")
        if message is None:
            continue
        chat_id = message["chat"]["id"] 
        text = message.get("text", "")
        handle_message(chat_id, text)

    if time.time() - last_check >= CHECK_INTERVAL:
        all_sites = load_sites()
        for chat_id, sites in all_sites.items():
            run_checks(chat_id, sites)
        last_check = time.time()

    time.sleep(2)