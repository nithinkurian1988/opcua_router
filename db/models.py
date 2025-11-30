from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, Float
from db.db_actions import Base

class OPCUANode(Base):
    __tablename__ = "opcua_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, index=True)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())