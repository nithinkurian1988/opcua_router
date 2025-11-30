from fastapi import APIRouter, Depends, Body
import db.db_actions as db_actions
from models import ReadAllResponse, ReadResponse
from models import WriteRequest, WriteResponse, ErrorResponse, DeleteResponse
from services.opcua_driver import opc_read, opc_write
from db.models import OPCUANode
from db.db_actions import init_models
from core.security import get_api_key

router = APIRouter()

# Initialize database models on router startup
@router.on_event("startup")
async def startup_event():
    await init_models()

@router.get("/read")
async def read_all_nodes(api_key: str = Depends(get_api_key)):
    # Get all OPC UA node data from the database
    records = await db_actions.get_all_nodes(OPCUANode)
    nodes_list = [{"node_id": record.node_id
                   , "value": record.value
                   , "timestamp": record.timestamp} for record in records]
    return ReadAllResponse(
        nodes=nodes_list,
        status="Success",
        message="All node values retrieved successfully",
        error=None
    )

@router.get("/read/{node_id}")
async def read_node(node_id: str, api_key: str = Depends(get_api_key)):
    # Get latest record of a specific node from the database or OPC UA server
    # add this to support both int and str node IDs in future
    if node_id.isdigit():
        node_id = int(node_id)
    record = await db_actions.get_node_by_id(OPCUANode, node_id)
    if not record:
        opc_response = await opc_read(node_id)
        if opc_response["status"] == "Success":
            value = opc_response["value"]
            # Save the new node to the database
            record = await db_actions.insert_node(node_id, value)
        else:
            return ErrorResponse(
                status="Failed",
                message="Node not found in database or OPC UA server",
                error=opc_response["error"]
            )
    return ReadResponse(
        status="Success",
        value=record.value,
        timestamp=record.timestamp.isoformat(),
        message="Node value retrieved successfully",
        error=None
    )

@router.post("/write")
async def write_node(request: WriteRequest = Body(...), api_key: str = Depends(get_api_key)):
    # Write a value to a specific OPC UA node and store in the database
    node_id = request.node_id
    value = request.value
    opc_response = await opc_write(node_id, value)
    if opc_response["status"] == "Success":
        # Save the new node to the database
        await db_actions.insert_node(node_id, value)
        return WriteResponse(
            status="Success",
            message="Node value written and stored successfully",
            error=None
        )
    else:
        return ErrorResponse(
            status="Failed",
            message="Error writing to OPC UA server",
            error=opc_response["error"]
        )

@router.put("/update/{node_id}")
async def update_node(node_id: str, api_key: str = Depends(get_api_key)):
    # Fetch a specific node from OPC UA server and update in the database
    # add this to support both int and str node IDs in future
    if node_id.isdigit():
        node_id = int(node_id)
    opc_response = await opc_read(node_id)
    if opc_response["status"] == "Success":
        value = opc_response["value"]
        # Update the node in the database
        updated_record = await db_actions.insert_node(node_id, value)
        if updated_record:
            return ReadResponse(
                status="Success",
                value=updated_record.value,
                timestamp=updated_record.timestamp.isoformat(),
                message="Node updated successfully",
                error=None
            )
    else:
        return ErrorResponse(
            status="Failed",
            message="Error reading from OPC UA server",
            error=opc_response["error"]
        )

@router.delete("/delete/{node_id}")
async def delete_node(node_id: str, api_key: str = Depends(get_api_key)):
    # Delete a specific OPC UA node data from the database
    # add this to support both int and str node IDs in future
    if node_id.isdigit():
        node_id = int(node_id)
    deleted_record = await db_actions.delete_node(OPCUANode, node_id)
    if deleted_record:
        return DeleteResponse(
            status="Success",
            message="Node deleted successfully",
            error=None
        )
    else:
        return DeleteResponse(
            status="Failed",
            message="Node not found",
            error="NotFoundError"
        )