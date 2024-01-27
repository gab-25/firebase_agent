import logging
import aiohttp

from aioshelly.block_device import COAP, BlockDevice
from aioshelly.rpc_device import RpcDevice, WsServer
from aioshelly.common import ConnectionOptions, get_info
from aioshelly.const import BLOCK_GENERATIONS, RPC_GENERATIONS
from aioshelly.exceptions import (
    DeviceConnectionError,
    FirmwareUnsupported,
    InvalidAuthError,
)


class Shelly:
    def __init__(self, host: str) -> None:
        self.options = ConnectionOptions(host)

    async def connect_device(self):
        async with aiohttp.ClientSession() as aiohttp_session:
            try:
                info_device = await get_info(aiohttp_session, self.options.ip_address)
                gen_device = info_device.get("gen", 1)
                if gen_device in BLOCK_GENERATIONS:
                    device = await self.__block_device(aiohttp_session)
                if gen_device in RPC_GENERATIONS:
                    device = await self.__rpc_device(aiohttp_session)
                logging.info("device %s connected!", device.name)
            except FirmwareUnsupported as err:
                logging.error("Device firmware not supported, error: %s", repr(err))
            except InvalidAuthError as err:
                logging.error("Invalid or missing authorization, error: %s", repr(err))
            except DeviceConnectionError as err:
                logging.error(
                    "Error connecting to %s, error: %s",
                    self.options.ip_address,
                    repr(err),
                )

    async def __block_device(self, aiohttp_session):
        async with COAP() as coap_context:
            return await BlockDevice.create(aiohttp_session, coap_context, self.options)

    async def __rpc_device(self, aiohttp_session):
        ws_context = WsServer()
        await ws_context.initialize(8123)

        return await RpcDevice.create(aiohttp_session, ws_context, self.options)
