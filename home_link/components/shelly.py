from pprint import pprint

import aiohttp

from aioshelly.block_device import COAP, BlockDevice
from aioshelly.rpc_device import RpcDevice, WsServer
from aioshelly.common import ConnectionOptions
from aioshelly.exceptions import (
    DeviceConnectionError,
    FirmwareUnsupported,
    InvalidAuthError,
)


class Shelly:
    def __init__(self) -> None:
        pass

    async def test_block_device(self):
        """Test Gen1 Block (CoAP) based device."""
        options = ConnectionOptions("192.168.1.165", "username", "password")

        async with aiohttp.ClientSession() as aiohttp_session, COAP() as coap_context:
            try:
                device = await BlockDevice.create(
                    aiohttp_session, coap_context, options
                )
            except FirmwareUnsupported as err:
                print(f"Device firmware not supported, error: {repr(err)}")
                return
            except InvalidAuthError as err:
                print(f"Invalid or missing authorization, error: {repr(err)}")
                return
            except DeviceConnectionError as err:
                print(f"Error connecting to {options.ip_address}, error: {repr(err)}")
                return

            for block in device.blocks:
                print(block)
                pprint(block.current_values())
                print()

    async def test_rpc_device(self):
        """Test Gen2/Gen3 RPC (WebSocket) based device."""
        options = ConnectionOptions("192.168.1.188", "username", "password")
        ws_context = WsServer()
        await ws_context.initialize(8123)

        async with aiohttp.ClientSession() as aiohttp_session:
            try:
                device = await RpcDevice.create(aiohttp_session, ws_context, options)
            except FirmwareUnsupported as err:
                print(f"Device firmware not supported, error: {repr(err)}")
                return
            except InvalidAuthError as err:
                print(f"Invalid or missing authorization, error: {repr(err)}")
                return
            except DeviceConnectionError as err:
                print(f"Error connecting to {options.ip_address}, error: {repr(err)}")
                return

            pprint(device.status)
