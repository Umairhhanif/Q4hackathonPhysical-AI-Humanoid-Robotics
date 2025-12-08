import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load the environment variables
load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

def get_safe_url(url):
    if not url:
        return "None"
    # Redact password
    try:
        if "@" in url:
            prefix = url.split("@")[0]
            suffix = url.split("@")[1]
            # Further split prefix to hide password
            if ":" in prefix:
                user = prefix.split("://")[1].split(":")[0]
                proto = prefix.split("://")[0]
                return f"{proto}://{user}:****@{suffix}"
        return url
    except:
        return "Error parsing URL"

print(f"Loaded DATABASE_URL: {get_safe_url(DATABASE_URL)}")

# Apply the same fix as in the codebase
if "postgresql://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

connect_args = {}
if "?sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]
    connect_args["ssl"] = "require"

async def check_host():
    try:
        engine = create_async_engine(DATABASE_URL, connect_args=connect_args)
        async with engine.connect() as conn:
            # Get database server configuration
            result = await conn.execute(text("SHOW server_version;"))
            version = result.scalar()
            print(f"✅ Connected to Postgres Server Version: {version}")
            
            # Check current database and user
            result = await conn.execute(text("SELECT current_database(), current_user, inet_server_addr();"))
            db, user, ip = result.fetchone()
            print(f"✅ Database: {db}")
            print(f"✅ User: {user}")
            # Neon usually waits for connection so IP might show cloud IP
            print(f"ℹ️  Server IP: {ip}")
            
            if "neon" in DATABASE_URL or "aws" in DATABASE_URL or "endpoint" in DATABASE_URL:
                 print("✅ CONFIRMED: Connection string points to a remote host (Neon/AWS).")
            else:
                 print("⚠️  WARNING: Connection string might be local.")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_host())
