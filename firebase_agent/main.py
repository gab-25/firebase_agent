import configparser
import firebase_admin
from firebase_admin import credentials
from firebase_agent import run


def main():
    cred = credentials.Certificate("./service_account_firebase.json")
    firebase_admin.initialize_app(cred)

    config = configparser.ConfigParser()
    config.read("./config")

    url = config["DEFAULT"]["SENSOR_URL"]
    token = config["DEFAULT"]["TOKEN"]
    run(url, token)


if __name__ == "__main__":
    main()
