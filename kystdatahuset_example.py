# user registration is required beforehand

# Det er ingen begrensninger i APIet men operasjoner som
# tar lang tid vil utløpe etter fire minutter. Når dette
# skjer er det ofte nyttig å dele opp data som etterspørres
# i mindre biter, f.eks. kortere tidsperioder eller
# mindre/færre geografiske områder.
import os

import requests
import json
from dotenv import load_dotenv

load_dotenv()

base_url = "https://kystdatahuset.no/ws/api"
auth_login_url = f"{base_url}/auth/login"

headersList = {
    "User-Agent": "",
    "accept": "*/*",
    "Content-Type": "application/json",
}

payload = json.dumps(
    {
        "username": os.environ["kystdatahuset_username"],
        "password": os.environ["kystdatahuset_password"],
    }
)

response = requests.request("POST", auth_login_url, data=payload, headers=headersList)
message = response.json()

jwt = message["data"]["JWT"]

imo_info_url = f"{base_url}/ship/combined/imo"
headersList = {
    "User-Agent": "",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}",
}
response = requests.get(imo_info_url + "/9224984", headers=headersList)
mmsi = response.json()["data"][0]["mmsi"]


reqUrl = f"{base_url}/ais/positions/for-mmsis-time"

headersList = {
    "User-Agent": "",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}",
}

payload = json.dumps(
    {"mmsiIds": [258500000], "start": "201701011345", "end": "201701041345"}
)

response = requests.request("POST", reqUrl, data=payload, headers=headersList)

print(response.text)
