import asyncio
import logging

from home_link.config import Config
from home_link.components.shelly import Shelly


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.info("start home-link")

    config = Config()

    shelly = Shelly()

    asyncio.run(shelly.test_block_device())
    asyncio.run(shelly.test_rpc_device())
