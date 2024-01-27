import asyncio
import logging

from home_link.config import Config, Platform
from home_link.components.shelly import Shelly


logging.basicConfig(
    format="%(asctime)s - %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


def main():
    logging.info("start home-link")

    config = Config()
    for device in config.devices:
        if device.platform == Platform.SHELLY:
            shelly_device = Shelly(device.host)
            asyncio.run(shelly_device.connect_device())
