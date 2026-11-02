import requests

def check_site(website):
    try:
        response = requests.get(website, timeout=5)

        if response.status_code == 200:
            return {"up": True, "status": response.status_code}
        else:
            return {"up": False, "status": response.status_code}

    except requests.exceptions.RequestException:
        return {"up": False, "status": None}

check = check_site("https://www.google.com")   

print(check)
print(check_site("https://this-site-does-not-exist-12345.com"))



