import requests

def check_site(website):
    try:
        response = requests.get(website, timeout=5)

        if 200 <= response.status_code < 300:
            return {"up": True, "status": response.status_code}
        else:
            return {"up": False, "status": response.status_code}

    except requests.exceptions.RequestException:
        return {"up": False, "status": None} 

sites = ["https://www.google.com", "https://this-site-does-not-exist-12345.com", "https://httpbin.org/status/500", "https://www.binance.com"]     
  
for number, site in enumerate(sites, start=1):
    check = check_site(site)
    if check["up"]:
        state = "UP"
    else:
        state = "DOWN"   
    if check["status"] is None:
        code = "No Response"
    else:
        code = check['status']    
    print(f"{number}. {site} - {state} {code}")





