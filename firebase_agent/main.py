import configparser
import firebase_admin
from firebase_admin import credentials

from firebase_agent import run
from firebase_agent.entity import Entity


def main():
    config = configparser.ConfigParser()
    config.read("./config")

    cred = credentials.Certificate(config["GENERAL"].get("firebase_cert"))
    firebase_admin.initialize_app(cred)

    entities: list[Entity] = [
        Entity(name=section, **config[section]) for section in filter(lambda s: s not in ["GENERAL"], config.sections())
    ]
    run(entities)


if __name__ == "__main__":
    main()
