import asyncio
import logging
from home_link.components import COMPONENTS
from home_link.components.base_component import BaseComponent

from home_link.config import Config


logging.basicConfig(
    format="%(asctime)s - %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def main():
    logging.info("start home-link")

    config = Config.instance()
    logging.getLogger().setLevel(config.log_level)

    logging.debug("load config: %s", config.__dict__)

    devices = list(config.devices.values())
    for device in devices:
        device_instance: BaseComponent = COMPONENTS.get(device.platform)(device)
        task = asyncio.create_task(device_instance.connect_device())
        await task


if __name__ == "__main__":
    asyncio.run(main())
