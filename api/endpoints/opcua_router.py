from fastapi import APIRouter, Depends, Body
import db.db_actions as db_actions
from models import ReadAllResponse, ReadResponse
from models import WriteRequest, WriteResponse, DeleteResponse
from services.opcua_driver import opc_read, opc_write
from db.models import OPCUANode
from core.security import get_api_key
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

router = APIRouter()

@router.get("/read")
async def read_all_nodes(api_key: str = Depends(get_api_key)):
    ''' Get all OPC UA nodes stored in the database '''
    records = await db_actions.get_all_nodes(OPCUANode)
    nodes_list = [{"node_id": record.node_id
                   , "value": record.value
                   , "timestamp": record.timestamp.isoformat()} for record in records]
    return ReadAllResponse(
        nodes=nodes_list,
        status="Success",
        message="All node values retrieved successfully",
        error=None
    )

@router.get("/read/{node_id}")
async def read_node(node_id: str, api_key: str = Depends(get_api_key)):
    ''' Get a specific OPC UA node value from the database or OPC UA server '''
    # added this to support both int and str node IDs in future
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
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail={
                    "status": "Failed",
                    "message": "Node not found in database or OPC UA server",
                    "error": opc_response["error"]
                }
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
    ''' Write a value to a specific OPC UA node and store it in the database '''
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
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
            "status": "Failed",
            "message": "Error writing to OPC UA server",
            "error": opc_response["error"]
            }
        )

@router.put("/update/{node_id}")
async def update_node(node_id: str, api_key: str = Depends(get_api_key)):
    ''' Fetch the latest value of a specific OPC UA node from
        the server and update it in the database '''
    # added this to support both int and str node IDs in future
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
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "status": "Failed",
                "message": "Error reading from OPC UA server",
                "error": opc_response["error"]
            }
        )

@router.delete("/delete/{node_id}")
async def delete_node(node_id: str, api_key: str = Depends(get_api_key)):
    ''' Delete a specific OPC UA node data from the database '''
    # added this to support both int and str node IDs in future
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
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "status": "Failed",
                "message": "Node not found in database",
                "error": "DeleteError"
            }
        )