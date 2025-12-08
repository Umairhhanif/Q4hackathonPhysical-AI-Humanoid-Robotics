from src.core.database import get_db, AsyncSessionLocal
from src.models.chat import InteractionLog
from datetime import datetime

async def log_interaction(
    user_query: str,
    bot_response: str,
    selected_text: str = None,
    latency_ms: int = 0,
    successful: bool = True
):
    """Log chat interaction to Postgres."""
    async with AsyncSessionLocal() as session:
        try:
            log_entry = InteractionLog(
                user_query=user_query,
                bot_response=bot_response,
                selected_text=selected_text,
                latency_ms=latency_ms,
                successful=successful,
                timestamp=datetime.utcnow()
            )
            session.add(log_entry)
            await session.commit()
        except Exception as e:
            print(f"Failed to log interaction: {e}")
            await session.rollback()
