import logging
import yaml


class Config:
    def __init__(self) -> None:
        logging.info("load configurations")
        self.__read_yaml()

    def __read_yaml(self):
        with open("config.yml", "r") as file:
            config_obj = yaml.safe_load(file)
            print(config_obj)
