import logging

from home_link.config import Config


def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s | %(message)s", datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info("start home-link")
    
    config = Config()

    logging.info("stop home-link")
