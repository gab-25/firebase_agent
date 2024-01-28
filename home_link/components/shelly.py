import logging
import datetime
import aiohttp

from aioshelly.block_device import COAP, BlockDevice, BlockUpdateType
from aioshelly.rpc_device import RpcDevice, WsServer, RpcUpdateType
from aioshelly.common import ConnectionOptions, get_info
from aioshelly.const import BLOCK_GENERATIONS, RPC_GENERATIONS
from aioshelly.exceptions import (
    DeviceConnectionError,
    FirmwareUnsupported,
    InvalidAuthError,
)

from home_link.config import Config, Device


class Shelly:
    def __init__(self, device: Device) -> None:
        self.options = ConnectionOptions(device.host, device.username, device.password)
        self.name = device.name
        self.gen = device.info.get("gen") if device.info is not None else None

    async def connect_device(self):
        async with aiohttp.ClientSession() as aiohttp_session:
            try:
                if self.gen is None:
                    logging.info("get info from device %s", self.name)
                    info_device = await get_info(
                        aiohttp_session, self.options.ip_address
                    )
                    self.gen = info_device.get("gen", 1)
                    Config.instance().set_device_info(
                        self.name, dict({**info_device, "gen": self.gen})
                    )

                if self.gen in BLOCK_GENERATIONS:
                    device = await self.__block_device(aiohttp_session)
                if self.gen in RPC_GENERATIONS:
                    device = await self.__rpc_device(aiohttp_session)
                logging.info("device %s connected!", self.name)
                device.subscribe_updates(device_updated)
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
        coap_context = COAP()
        await coap_context.initialize()

        return await BlockDevice.create(aiohttp_session, coap_context, self.options)

    async def __rpc_device(self, aiohttp_session):
        ws_context = WsServer()
        await ws_context.initialize(8123)

        return await RpcDevice.create(aiohttp_session, ws_context, self.options)


def device_updated(
    cb_device: BlockDevice | RpcDevice,
    update_type: BlockUpdateType | RpcUpdateType,
) -> None:
    print()
    logging.info(
        "%s Device updated! (%s)",
        datetime.datetime.now().strftime("%H:%M:%S"),
        update_type,
    )
    print(cb_device)
