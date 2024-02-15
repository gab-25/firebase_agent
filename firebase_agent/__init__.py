import datetime
import requests
from firebase_admin import firestore

from firebase_agent.entity import Entity


def run(entities: list[Entity]):
    db = firestore.client()

    for entity in entities:
        headers = {
            "content-type": "application/json",
        }
        if entity.token is not None:
            headers["Authorization"] = f"Bearer {entity.token}"
        response = requests.get(entity.url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"error http request, stauts code: {response.status_code}")
        data = response.json()

        doc = {"ts": datetime.datetime.utcnow()}
        if entity.value_prop is not None:
            doc["value"] = data[entity.value_prop]
            doc["data"] = data
        else:
            doc["value"] = data
        db.collection("energy").add(doc)
        print("add to firestore collection, document:", doc)
