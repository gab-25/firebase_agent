import datetime
import base64
import requests
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from firebase_agent.config import ConfigEntity
from firebase_agent.entity import EntityAggregate, Entity


def run(config_entities: list[ConfigEntity]):
    db = firestore.client()

    for config_entity in config_entities:
        if isinstance(config_entity, ConfigEntity):
            headers = {
                "content-type": "application/json",
            }
            if config_entity.token is not None:
                headers["Authorization"] = "Bearer " + config_entity.token
            if config_entity.username is not None and config_entity.password is not None:
                headers["Authorization"] = "Basic " + base64.b64encode(
                    f"{config_entity.username}:{config_entity.password}"
                )
            response = requests.get(config_entity.url, headers=headers, timeout=10)
            if response.status_code != 200:
                raise Exception(f"error http request, stauts code: {response.status_code}")
            data = response.json()

        coll_entity_ref = db.collection(config_entity.name.lower())
        coll_entity_aggregate_ref = db.collection(f"{config_entity.name.lower()}_aggregate")

        entity = Entity()
        if config_entity.value_prop is not None:
            entity.value = data[config_entity.value_prop]
            entity.data = data
        else:
            entity.value = data
        doc_ref = coll_entity_ref.add(entity.to_dict())
        print(f"add to firestore collection: {coll_entity_ref.id}, document: {doc_ref[1].id}")

        if config_entity.create_aggregate is not None:
            start_today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            end_today = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            docs_query = (
                coll_entity_ref.where(filter=FieldFilter("ts", ">=", start_today))
                .where(filter=FieldFilter("ts", "<=", end_today))
                .order_by("ts")
            )

            dict_entity_aggregate: dict[datetime.date | datetime.datetime, EntityAggregate] = {}
            for doc_query in docs_query.get():
                entity = Entity(**doc_query.to_dict())
                ts_key_daily = entity.ts.date()
                if ts_key_daily not in dict_entity_aggregate:
                    dict_entity_aggregate[ts_key_daily] = EntityAggregate(
                        start_ts=datetime.datetime.combine(ts_key_daily, datetime.time.min),
                        end_ts=datetime.datetime.combine(ts_key_daily, datetime.time.max),
                    )
                current_aggregate_daily = dict_entity_aggregate.get(ts_key_daily)
                current_aggregate_daily.add_value(entity.value)
                ts_key_hourly = datetime.datetime.combine(
                    entity.ts.date(), datetime.time(hour=entity.ts.time().hour, minute=0, second=0, microsecond=0)
                )
                if ts_key_hourly not in dict_entity_aggregate:
                    dict_entity_aggregate[ts_key_hourly] = EntityAggregate(
                        start_ts=ts_key_hourly, end_ts=ts_key_hourly + datetime.timedelta(hours=1)
                    )
                current_aggregate_hourly = dict_entity_aggregate.get(ts_key_daily)
                current_aggregate_hourly.add_value(entity.value)
            for entity_aggregate in dict_entity_aggregate.values():
                doc_entity_aggregate_exist = coll_entity_aggregate_ref.where(filter=FieldFilter("start_ts", "==", entity_aggregate.start_ts)).where(
                    filter=FieldFilter("end_ts", "==", entity_aggregate.end_ts)
                ).limit(1).get()
                if len(doc_entity_aggregate_exist) == 0:
                    doc_ref = coll_entity_aggregate_ref.add(entity_aggregate.to_dict())
                    print(f"add to firestore collection: {coll_entity_aggregate_ref.id}, document: {doc_ref[1].id}")
                if len(doc_entity_aggregate_exist) == 1 and entity_aggregate.count != doc_entity_aggregate_exist[0].get("count"):
                    coll_entity_aggregate_ref.document(doc_entity_aggregate_exist[0].id).update(entity_aggregate.to_dict())
                    print(f"update to firestore collection: {coll_entity_aggregate_ref.id}, document: {doc_entity_aggregate_exist[0].id}")
