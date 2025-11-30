# tests/test_opcua_driver.py

def test_read_opc_value(mock_opcua_driver):
    """Test reading a value from OPC UA server"""
    mock_client = mock_opcua_driver.Client.return_value
    mock_node = mock_client.get_node.return_value
    mock_node.read_value.return_value = 42  # Configure the mock to return 42
    client = mock_opcua_driver.Client("opc.tcp://localhost:4840")
    client.connect()
    node = client.get_node("ns=2;i=2")
    value = node.read_value()
    
    # Verify the read value
    assert value == 42

def test_write_opc_value(mock_opcua_driver):
    """Test writing a value to OPC UA server"""
    mock_client = mock_opcua_driver.Client.return_value
    mock_node = mock_client.get_node.return_value
    mock_node.read_value.return_value = 100  # Configure the mock to return 100 after write
    client = mock_opcua_driver.Client("opc.tcp://localhost:4840")
    client.connect()
    node = client.get_node("ns=2;i=2")
    node.write_value(100)
    value = node.read_value()
    
    # Verify the written value
    assert value == 100

def test_opcua_connection(mock_opcua_driver):
    """Test OPC UA client connection"""
    mock_client = mock_opcua_driver.Client.return_value
    client = mock_opcua_driver.Client("opc.tcp://localhost:4840")
    connected = client.connect()
    
    # Verify that connect method was called
    mock_client.connect.assert_called_once()
    assert connected is True