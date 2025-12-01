import logging
from asyncua import Client
from fastapi import HTTPException
from core.config import OPC_URL, OPC_USERNAME, OPC_PASSWORD, OPC_NAMESPACE

logger = logging.getLogger(__name__)


async def opc_write(node_id, value):
    client = Client(OPC_URL, watchdog_intervall=20)
    client.set_user(OPC_USERNAME)
    client.set_password(OPC_PASSWORD)
    # Currently supporting namespace index 2 and integer node IDs only.
    node_id = f"ns={OPC_NAMESPACE};i={node_id}"
    try:
        logger.info("Connecting to OPC UA server")
        async with client:
            node = client.get_node(node_id)
            await node.write_value(value)
            read_value = await node.read_value()
            if read_value == value:
                return {
                    "status": "Success",
                    "message": "Value written successfully",
                    "error": None,
                }
            else:
                return {
                    "status": "Failed",
                    "error": "OPCWriteError",
                }
    except Exception as e:
        logger.error(f"Error writing OPC data: {e}")
    finally:
        logger.info("Disconnected from OPC UA server")
        return {
            "status": "Failed",
            "error": "OPCWriteError",
        }


async def opc_read(nodeid):
    client = Client(OPC_URL, watchdog_intervall=20)
    client.set_user(OPC_USERNAME)
    client.set_password(OPC_PASSWORD)
    # Currently supporting namespace index 2 and integer node IDs only.
    node_id = f"ns={OPC_NAMESPACE};i={nodeid}"
    try:
        logger.info("Connecting to OPC UA server for reading")
        async with client:
            node = client.get_node(node_id)
            value = await node.read_value()
            return {
                "status": "Success",
                "value": value,
                "message": "Value read successfully",
                "error": None,
            }
    except Exception as e:
        logger.error(f"Error reading OPC data: {e}")
    finally:
        logger.info("Disconnected from OPC UA server")
        return {
            "status": "Failed",
            "error": "OPCReadError",
        }
