import requests

def get_location_info():
    return requests.get("http://freegeoip.app/json/").json()

if __name__ == "__main__":
    print(get_location_info())
