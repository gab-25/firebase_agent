import asyncio
import logging

from home_link.config import Config, Device, Platform
from home_link.components.shelly import Shelly


logging.basicConfig(
    format="%(asctime)s - %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def __init_devices(devices: list[Device]):
    for device in devices:
        if device.platform == Platform.SHELLY:
            shelly_device = Shelly(device)
            await shelly_device.connect_device()

    while True:
        await asyncio.sleep(0.1)


def main():
    logging.info("start home-link")

    config = Config.instance()

    devices = list(config.devices.values())
    asyncio.run(__init_devices(devices))


if __name__ == "__main__":
    main()
