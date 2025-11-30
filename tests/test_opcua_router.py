# tests/test_opcua_router.py
import pytest
from starlette.status import HTTP_200_OK
from services import opcua_driver

TEST_API_KEY_NAME="API-KEY"
TEST_API_KEY="1234567890abcdef"

pytestmark = pytest.mark.usefixtures("mock_opcua_driver")

def test_read_node_success(client, db_session, mock_opcua_driver):
    """Test reading a node that exists in the database"""
    # Pre-insert a node into the test database
    from db.models import OPCUANode
    from datetime import datetime, timezone
    test_node = OPCUANode(node_id=1, value=25.5, timestamp=datetime.now(timezone.utc))
    db_session.add(test_node)
    db_session.commit()

    response = client.get(
        "/opcua/read/1",
        headers={
            "accept": "application/json",
            TEST_API_KEY_NAME: TEST_API_KEY
        }
    )

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["status"] == "Success"
    assert data["value"] == 25.5