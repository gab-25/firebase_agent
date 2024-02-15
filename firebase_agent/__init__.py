import datetime
import requests
from firebase_admin import firestore


def run(url: str, token: str = None):
    db = firestore.client()

    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    ts = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    doc = {"ts": ts, "value": data["state"], "data": data}

    coll_ref = db.collection("energy")
    coll_ref.add(doc)
    print("add to firestore collection, document:", doc)
