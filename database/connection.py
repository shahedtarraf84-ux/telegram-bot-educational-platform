"""
MongoDB Connection - Optimized for Vercel Serverless
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from loguru import logger

from config.settings import settings
from database.models.user import User
from database.models.video import Video
from database.models.assignment import Assignment
from database.models.notification import Notification


class Database:
    """Database connection manager - Serverless optimized"""
    client: AsyncIOMotorClient = None
    beanie_initialized: bool = False
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB with retry logic and caching for serverless"""
        # Return cached connection if already initialized
        if cls.client is not None and cls.beanie_initialized:
            logger.debug("Reusing cached MongoDB connection")
            return True
        
        for attempt in range(1, cls.MAX_RETRIES + 1):
            try:
                # Debug: log MongoDB URI (masked) and DB name
                masked_uri = settings.MONGODB_URL
                try:
                    if "@" in settings.MONGODB_URL and "://" in settings.MONGODB_URL:
                        prefix, rest = settings.MONGODB_URL.split("://", 1)
                        creds_and_host = rest.split("@", 1)
                        if len(creds_and_host) == 2:
                            _, host_part = creds_and_host
                            masked_uri = f"{prefix}://***:***@{host_part}"
                except Exception as mask_error:
                    logger.error(f"Failed to mask MongoDB URI for debug logging: {mask_error}")
                    print(f"ERROR: Failed to mask MongoDB URI: {mask_error}", flush=True)
                
                logger.info(f"[Attempt {attempt}/{cls.MAX_RETRIES}] Connecting to MongoDB: {masked_uri}, db={settings.MONGODB_DB_NAME}")
                print(f"[Attempt {attempt}/{cls.MAX_RETRIES}] Connecting to MongoDB: {masked_uri}, db={settings.MONGODB_DB_NAME}", flush=True)
                
                # Create client with optimized timeouts for Vercel
                # Increased timeouts to handle cold starts
                cls.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=15000,  # 15s for cold start
                    connectTimeoutMS=20000,          # 20s for cold start
                    socketTimeoutMS=20000,           # 20s for operations
                    maxPoolSize=10,                  # Connection pooling
                    minPoolSize=1,                   # Minimum connections
                    maxIdleTimeMS=45000,             # Close idle connections after 45s
                )
                
                # Test the connection with ping
                await cls.client.admin.command('ping')
                logger.info("MongoDB ping successful")
                print("MongoDB ping successful", flush=True)
                
                # Initialize Beanie only once
                if not cls.beanie_initialized:
                    await init_beanie(
                        database=cls.client[settings.MONGODB_DB_NAME],
                        document_models=[
                            User,
                            Video,
                            Assignment,
                            Notification,
                        ]
                    )
                    cls.beanie_initialized = True
                
                logger.info("MongoDB connected successfully and Beanie initialized")
                print("MongoDB connected successfully and Beanie initialized", flush=True)
                return True
                
            except Exception as e:
                error_msg = f"[Attempt {attempt}/{cls.MAX_RETRIES}] MongoDB connection failed: {repr(e)}"
                logger.error(error_msg)
                print(f"ERROR: {error_msg}", flush=True)
                
                if attempt < cls.MAX_RETRIES:
                    logger.info(f"Retrying in {cls.RETRY_DELAY} seconds...")
                    print(f"Retrying in {cls.RETRY_DELAY} seconds...", flush=True)
                    await asyncio.sleep(cls.RETRY_DELAY)
                else:
                    error_msg = "Max retries reached. Could not connect to MongoDB."
                    logger.error(error_msg)
                    print(f"ERROR: {error_msg}", flush=True)
                    raise
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")


# Convenience function
async def init_db():
    """Initialize database"""
    await Database.connect()


async def close_db():
    """Close database"""
    await Database.close()
