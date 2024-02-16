import configparser
import firebase_admin
from firebase_admin import credentials

from firebase_agent import run
from firebase_agent.config import ConfigEntity, ConfigEntityType


def main():
    config = configparser.ConfigParser()
    config.read("./config")

    cred = credentials.Certificate(config["GENERAL"].get("firebase_cert"))
    firebase_admin.initialize_app(cred)

    config_entities: list[ConfigEntity] = []
    for section in filter(lambda s: s not in ["GENERAL"], config.sections()):
        config_entity = ConfigEntity(
            type=ConfigEntityType(config[section].get("type")),
            name=section,
            url=config[section].get("url"),
            username=config[section].get("username"),
            password=config[section].get("password"),
            token=config[section].get("token"),
            value_prop=config[section].get("value_prop"),
            create_aggregate=config[section].getboolean("create_aggregate"),
        )
        config_entities.append(config_entity)
    run(config_entities)


if __name__ == "__main__":
    main()
