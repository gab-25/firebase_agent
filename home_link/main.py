import asyncio
import logging

from websockets import serve

from home_link.config import Config


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.info("start home-link")

    config = Config()

    asyncio.run(start_serve())

    logging.info("stop home-link")


async def start_serve():
    async with serve(echo, "localhost", 5000):
        await asyncio.Future()


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
