import asyncio
import logging

from home_link.config import Config, Device, Platform
from home_link.components.shelly import Shelly


logging.basicConfig(
    format="%(asctime)s - %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def _init_devices(devices: list[Device]):
    while True:
        for device in devices:
            if device.platform == Platform.SHELLY:
                shelly_device = Shelly(device)
                await shelly_device.connect_device()
            if device.platform == Platform.MQTT:
                pass
            if device.platform == Platform.HTTP:
                pass

        await asyncio.sleep(10)


def main():
    logging.info("start home-link")

    config = Config.instance()
    logging.getLogger().setLevel(config.log_level)

    devices = list(config.devices.values())
    asyncio.run(_init_devices(devices))


if __name__ == "__main__":
    main()
