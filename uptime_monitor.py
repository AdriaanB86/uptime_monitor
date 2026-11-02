import requests
from datetime import datetime

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

def get_code(check):
    if check["status"] is None:
        return "No Response"
    else:
        return check['status']             

sites = ["https://www.google.com", "https://this-site-does-not-exist-12345.com", "https://httpbin.org/status/500", "https://www.binance.com"]     

for number, site in enumerate(sites, start=1):
    check = check_site(site)
    log_result(site, check)
    state = get_state(check)
    code = get_code(check)
      
    print(f"{number}. {site} - {state} {code}")