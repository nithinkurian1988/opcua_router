from pydantic import BaseModel, Field


class WriteResponse(BaseModel):
    status: str
    message: str
    error: str | None = None


class WriteRequest(BaseModel):
    '''
    Request model for writing a value to an OPC UA node.
    Example Request Body:
    {
        "node_id": 123,
        "value": 56.78
    }
    '''
    node_id: int = Field(..., description="currently supporting integer node IDs only.")
    value: float = Field(..., description="The value to write to the node.")

    class Config:
        extra = "forbid"


class ReadResponse(BaseModel):
    status: str
    value: float
    timestamp: str
    message: str
    error: str | None = None


class ReadAllResponse(BaseModel):
    nodes: list[dict]
    status: str
    message: str
    error: str | None = None


class DeleteResponse(BaseModel):
    status: str
    message: str
    error: str | None = None


class ErrorResponse(BaseModel):
    status: str
    message: str
    error: str | None = None
