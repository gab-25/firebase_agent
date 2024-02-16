import firebase_admin
from firebase_admin import credentials

from firebase_agent import run
from firebase_agent.config import config_general, config_entities


def main():
    cred = credentials.Certificate(config_general.get("firebase_cert"))
    firebase_admin.initialize_app(cred)

    run(config_entities)


if __name__ == "__main__":
    main()
