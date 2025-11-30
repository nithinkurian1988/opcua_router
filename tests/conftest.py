import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from collections.abc import Generator
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pytest import fixture
from db.db_actions import get_session
from db.models import Base
from main import create_app
from sqlalchemy import create_engine, text
import asyncio
import sys

ROUTER_MODULE_PATH = "api.endpoints.opcua_router"

# ---------- Windows event loop fix ----------
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@fixture(scope="function")
def app() -> FastAPI:
    '''Provides a FastAPI app instance for tests.'''
    return create_app()

# First, connect to the default 'postgres' database to create the test database if needed
def setup_test_database():
    """Create test database if it doesn't exist and create tables"""
    # Connect to default postgres database
    default_db_url = "postgresql://postgres:Nkk%400475@127.0.0.1:5432/postgres"
    default_engine = create_engine(default_db_url, isolation_level="AUTOCOMMIT")
    
    try:
        with default_engine.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = 'opc_test_db'")
            )
            if not result.fetchone():
                # Create the database
                conn.execute(text("CREATE DATABASE opc_test_db"))
                print("Test database 'opc_test_db' created successfully")
    finally:
        default_engine.dispose()
    
    # Connect to the test database and create tables
    test_db_url = "postgresql://postgres:Nkk%400475@127.0.0.1:5432/opc_test_db"
    test_engine = create_engine(test_db_url)
    
    try:
        # Create all tables defined in the Base metadata
        Base.metadata.create_all(bind=test_engine)
        print("Database tables created successfully")
        return test_engine
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

# Setup the test database and get the engine
engine = setup_test_database()

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False
)

@fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    '''Provides a database session for tests.'''
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    '''Provides a TestClient for the FastAPI app with overridden DB session'''
    def get_test_session() -> Generator[Session, None, None]:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# @fixture(scope="function")
# def mock_opcua_driver() -> Generator[MagicMock, None, None]:
#     '''Provides a mock for the opcua_driver module with configured behaviors'''
#     with patch(f"{ROUTER_MODULE_PATH}.opc_read") as mock_read, \
#          patch(f"{ROUTER_MODULE_PATH}.opc_write") as mock_write:
        
#         # Configure how the fake OPC read behaves
#         # Configure how the fake OPC read behaves
#         # Create a shared variable to store the written value
#         written_value = {"value": 25.5}  # default value
        
#         def mock_read_side_effect(*args, **kwargs):
#             return {
#             "status": "Success",
#             "value": written_value["value"],
#             "message": "Value read successfully",
#             "error": None,
#             }
        
#         def mock_write_side_effect(node_id, value, *args, **kwargs):
#             written_value["value"] = value
#             return True
        
#         mock_read.side_effect = mock_read_side_effect
#         mock_write.side_effect = mock_write_side_effect

#         # Yield both mocks if you want to inspect them in tests
#         yield {
#             "opc_read": mock_read,
#             "opc_write": mock_write,
#         }

@fixture(scope="function")
def mock_opcua_driver():
    """
    Module-style mock for services.opcua_driver
    """
    with patch("services.opcua_driver") as mock:
        mock_client = MagicMock()
        mock_client.connect.return_value = True

        mock_node = MagicMock()
        mock_node.read_value = MagicMock()
        mock_client.get_node.return_value = mock_node

        mock_node.write_value = MagicMock(return_value=True)

        mock.Client = MagicMock(return_value=mock_client)

        yield mock