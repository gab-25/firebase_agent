import asyncio
import logging
from home_link.components import platforms
from home_link.components.abstract_component import AbstractComponent

from home_link.config import Config


logging.basicConfig(
    format="%(asctime)s - %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def _connect_device(device_instance: AbstractComponent):
    while True:
        await device_instance.connect()
        if device_instance.interval is not None:
            await asyncio.sleep(device_instance.interval)
        else:
            break


def main():
    logging.info("start home-link")

    config = Config.instance()
    logging.getLogger().setLevel(config.log_level)

    logging.debug("load config: %s", config.__dict__)

    event_loop = asyncio.get_event_loop()

    devices = list(config.devices.values())
    for device in devices:
        device_instance: AbstractComponent = platforms.get(device.platform)(device)
        asyncio.ensure_future(_connect_device(device_instance))

    event_loop.run_forever()


if __name__ == "__main__":
    main()
