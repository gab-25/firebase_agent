import datetime
import requests
import firebase_admin
from firebase_admin import credentials, firestore

HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyNmFkY2JiMTZiNGU0ZDRhYjc1OTJlNWE0ZThlNTQ4YiIsImlhdCI6MTcwNzk5MDk2NywiZXhwIjoyMDIzMzUwOTY3fQ.eTLEJXJIy-98rfmjCEoDvAqJa8Sj66f3yd7HLBFbZCw"
HA_SENSOR_URL = "https://ha.gabprojects.dev:8123/api/states/sensor.shellyem_ba51f9_channel_1_energy"
INIT_APP = False


def main():
    if INIT_APP:
        cred = credentials.Certificate("./service_account_firebase.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    response = requests.get(HA_SENSOR_URL, headers=headers)
    data = response.json()

    ts = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    doc = {"ts": ts, "value": data["state"], "data": data}

    coll_ref = db.collection("energy")
    coll_ref.add(doc)
    print("add to firestore collection, document:", doc)


if __name__ == "__main__":
    main()
