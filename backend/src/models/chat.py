from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from src.core.database import Base

class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    successful = Column(Boolean, default=True)