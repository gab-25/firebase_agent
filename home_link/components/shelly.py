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
from home_link.components.base_component import BaseComponent

from home_link.config import Config, Device


class Shelly(BaseComponent):
    def __init__(self, device: Device):
        super().__init__(device)
        self.options = ConnectionOptions(device.host, device.username, device.password)
        self.gen = device.info.get("gen") if device.info is not None else None

    async def connect_device(self):
        async with aiohttp.ClientSession() as aiohttp_session:
            try:
                config = Config.instance()
                if self.gen is None:
                    logging.info("get info from device %s", self.name)
                    info_device = await get_info(aiohttp_session, self.options.ip_address)
                    self.gen = info_device.get("gen", 1)

                if self.gen in BLOCK_GENERATIONS:
                    logging.info("get status from device %s", self.name)
                    device = await self._block_device(aiohttp_session)
                    state = {block.description: block.current_values() for block in device.blocks}
                if self.gen in RPC_GENERATIONS:
                    logging.info("connect to device %s", self.name)
                    device = await self._rpc_device(aiohttp_session)
                    state = device.status
                info = dict({**device.shelly, "gen": self.gen})
                config.update_device(device_name=self.name, info=info, state=state)
            except FirmwareUnsupported:
                logging.error("Device %s firmware not supported", self.name)
            except InvalidAuthError:
                logging.error("Invalid or missing authorization from device %s", self.name)
            except DeviceConnectionError:
                logging.error("Error connecting to %s ip: %s", self.name, self.options.ip_address)

    async def _block_device(self, aiohttp_session):
        coap_context = COAP()
        await coap_context.initialize()

        return await BlockDevice.create(aiohttp_session, coap_context, self.options)

    async def _rpc_device(self, aiohttp_session):
        ws_context = WsServer()
        await ws_context.initialize(8123)

        return await RpcDevice.create(aiohttp_session, ws_context, self.options)
