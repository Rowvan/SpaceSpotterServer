import requests, json

from structures import *

SERVER_URL = "http://10.64.128.73:80"

requests.post(
    f"{SERVER_URL}",
    auth = ("SpaceSpotterAdmin", "changeme"),
)

def post_get():
    return requests.post(
        f"{SERVER_URL}/api/get/space",
        auth = ("YCPAdmin", "changeme7"),
        json = {
            "LOTID": 0,
            "SPACEID": 1
        }
    )

requests.post(
    f"{SERVER_URL}/api/update/space",
    auth = ("YCPAdmin", "changeme7"),
    json = {
        "LOTID": 0,
        "SPACEID": 1,
        "STATUS": {
            "status": 0,
            "time": 0
        }
    }
)

response = requests.post(
    f"{SERVER_URL}/api/get/space",
    auth = ("YCPAdmin", "changeme7"),
    json = {
        "LOTID": 0,
        "SPACEID": 1
    }
)  

print(response.content)

data = json.loads(response.content)

space_recived = Space.from_dict(data)