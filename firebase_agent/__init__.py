import datetime
import base64
import requests
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from firebase_agent.config import ConfigEntity, ConfigEntity, ConfigEntityAggregateType
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
        doc_ref = coll_entity_ref.add(entity.__dict__)
        print(f"add to firestore collection: {coll_entity_ref.id}, document: {doc_ref[1].id}")

        if config_entity.create_aggregate is not None:
            start_today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            end_today = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            docs_query = (
                coll_entity_ref.where(filter=FieldFilter("ts", ">=", start_today))
                .where(filter=FieldFilter("ts", "<=", end_today))
                .order_by("ts")
            )

            dict_entity_aggregate: dict[datetime.datetime, EntityAggregate] = {}
            for doc_query in docs_query.get():
                entity = Entity(**doc_query.to_dict())
                if config_entity.create_aggregate == ConfigEntityAggregateType.DAILY:
                    ts_key = datetime.datetime.combine(
                        entity.ts.date(), datetime.time(hour=0, minute=0, second=0, microsecond=0)
                    )
                if config_entity.create_aggregate == ConfigEntityAggregateType.HOURLY:
                    ts_key = datetime.datetime.combine(
                        entity.ts.date(), datetime.time(hour=entity.ts.time().hour, minute=0, second=0, microsecond=0)
                    )
                if config_entity.create_aggregate == ConfigEntityAggregateType.MINUTE:
                    ts_key = datetime.datetime.combine(
                        entity.ts.date(),
                        datetime.time(
                            hour=entity.ts.time().hour, minute=entity.ts.time().minute, second=0, microsecond=0
                        ),
                    )
                if ts_key not in dict_entity_aggregate:
                    dict_entity_aggregate[ts_key] = EntityAggregate(ts_key)
                current_aggregate = dict_entity_aggregate.get(ts_key)
                current_aggregate.add_value(entity.value)
            for entity_aggregate in dict_entity_aggregate.values():
                doc_ref = coll_entity_aggregate_ref.add(entity_aggregate.__dict__)
                print(f"add to firestore collection: {coll_entity_aggregate_ref.id}, document: {doc_ref[1].id}")
