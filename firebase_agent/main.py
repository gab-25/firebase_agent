import configparser
import firebase_admin
from firebase_admin import credentials

from firebase_agent import run
from firebase_agent.entity import Entity, HttpEntity, EntityType


def main():
    config = configparser.ConfigParser()
    config.read("./config")

    cred = credentials.Certificate(config["GENERAL"].get("firebase_cert"))
    firebase_admin.initialize_app(cred)

    entities: list[Entity] = []
    sections_filtered = filter(lambda s: s not in ["GENERAL"], config.sections())
    for section in sections_filtered:
        entity_type = config[section]["type"]
        del config[section]["type"]
        if entity_type == EntityType.HTTP.value:
            entities.append(HttpEntity(name=section, **config[section]))
    run(entities)


if __name__ == "__main__":
    main()
