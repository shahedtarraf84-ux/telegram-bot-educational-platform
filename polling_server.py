"""
Polling Mode Server - Alternative to Webhook
This runs the bot in polling mode instead of webhook mode.
Useful when webhook is not working or not available.
"""

import os
import asyncio
from loguru import logger

from config.settings import settings
from bot.main import create_application
from database.connection import Database

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or settings.TELEGRAM_BOT_TOKEN
MONGODB_URL = os.environ.get("MONGODB_URL") or settings.MONGODB_URL
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME") or settings.MONGODB_DB_NAME


async def main():
    """Start bot in polling mode"""
    
    logger.info("🚀 Starting Educational Platform Bot in POLLING MODE...")
    print("🚀 Starting Educational Platform Bot in POLLING MODE...", flush=True)
    
    # Initialize database
    try:
        logger.info("📡 Initializing MongoDB connection...")
        print("📡 Initializing MongoDB connection...", flush=True)
        await Database.connect()
        logger.info("✅ MongoDB connection established")
        print("✅ MongoDB connection established", flush=True)
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {repr(e)}", exc_info=True)
        print(f"❌ Failed to initialize database: {repr(e)}", flush=True)
    
    # Create and start bot
    try:
        logger.info("🤖 Initializing Telegram bot...")
        print("🤖 Initializing Telegram bot...", flush=True)
        
        telegram_app = create_application()
        
        # Initialize bot
        await telegram_app.initialize()
        await telegram_app.start()
        logger.info("✅ Telegram bot initialized")
        print("✅ Telegram bot initialized", flush=True)
        
        # Delete webhook if exists (to switch from webhook to polling)
        try:
            webhook_info = await telegram_app.bot.get_webhook_info()
            if webhook_info.url:
                logger.info(f"🗑️ Deleting old webhook: {webhook_info.url}")
                print(f"🗑️ Deleting old webhook: {webhook_info.url}", flush=True)
                await telegram_app.bot.delete_webhook(drop_pending_updates=False)
                logger.info("✅ Old webhook deleted")
                print("✅ Old webhook deleted", flush=True)
        except Exception as e:
            logger.warning(f"⚠️ Could not delete webhook: {repr(e)}")
            print(f"⚠️ Could not delete webhook: {repr(e)}", flush=True)
        
        # Start polling
        logger.info("🔄 Starting polling mode...")
        print("🔄 Starting polling mode...", flush=True)
        print("✅ Bot is now running in POLLING MODE", flush=True)
        print("✅ Bot will receive messages via polling", flush=True)
        
        await telegram_app.run_polling(
            allowed_updates=None,  # Get all updates
            drop_pending_updates=False,  # Don't drop pending updates
            close_loop=False
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {repr(e)}", exc_info=True)
        print(f"❌ Failed to start bot: {repr(e)}", flush=True)
        raise
    finally:
        # Cleanup
        try:
            await telegram_app.stop()
            await telegram_app.shutdown()
        except:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("Bot stopped by user", flush=True)
    except Exception as e:
        logger.error(f"Fatal error: {repr(e)}", exc_info=True)
        print(f"Fatal error: {repr(e)}", flush=True)
