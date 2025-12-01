"""Unified server entrypoint for Educational Platform.

Runs:
- Telegram bot in webhook mode
- Admin dashboard
- Background notification scheduler

Provides a health check at root path "/".
"""

import os
import asyncio

from fastapi import FastAPI, Request
from loguru import logger
from telegram import Update

from config.settings import settings
from bot.main import create_application
from admin_dashboard.app import app as dashboard_app
from utils.notifications import NotificationScheduler

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or settings.TELEGRAM_BOT_TOKEN
MONGODB_URL = os.environ.get("MONGODB_URL") or settings.MONGODB_URL
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME") or settings.MONGODB_DB_NAME

# Get webhook URL - try multiple sources
BOT_WEBHOOK_URL = os.environ.get("BOT_WEBHOOK_URL") or settings.BOT_WEBHOOK_URL

# Log the webhook URL
print(f"🔗 BOT_WEBHOOK_URL: {BOT_WEBHOOK_URL}", flush=True)
if not BOT_WEBHOOK_URL:
    print("⚠️ WARNING: BOT_WEBHOOK_URL is not set!", flush=True)


# Create Telegram bot application
telegram_app = create_application()

# Main FastAPI application
app = FastAPI(title="Educational Platform - Unified Server")

# Mount admin dashboard under /admin
app.mount("/admin", dashboard_app)


@app.on_event("startup")
async def on_startup() -> None:
    """Startup logic for unified server."""
    logger.info("🚀 Starting Educational Platform server...")
    print("🚀 Starting Educational Platform server...", flush=True)
    
    # Initialize database connection FIRST
    try:
        from database.connection import Database
        logger.info("📡 Initializing MongoDB connection...")
        print("📡 Initializing MongoDB connection...", flush=True)
        await Database.connect()
        logger.info("✅ MongoDB connection established")
        print("✅ MongoDB connection established", flush=True)
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {repr(e)}", exc_info=True)
        print(f"❌ Failed to initialize database: {repr(e)}", flush=True)
        # Don't raise - allow server to start even if DB fails initially
        print("⚠️ Server continuing without database connection", flush=True)
    
    # Start Telegram bot (webhook mode)
    try:
        logger.info("🤖 Initializing Telegram bot...")
        print("🤖 Initializing Telegram bot...", flush=True)
        await telegram_app.initialize()
        await telegram_app.start()
        logger.info("✅ Telegram bot initialized")
        print("✅ Telegram bot initialized", flush=True)

        webhook_url = BOT_WEBHOOK_URL
        if webhook_url:
            try:
                # First, get current webhook info
                webhook_info = await telegram_app.bot.get_webhook_info()
                logger.info(f"Current webhook: {webhook_info.url}")
                print(f"Current webhook: {webhook_info.url}", flush=True)
                
                # Delete old webhook if it exists
                if webhook_info.url:
                    await telegram_app.bot.delete_webhook(drop_pending_updates=True)
                    logger.info("✅ Old webhook deleted")
                    print("✅ Old webhook deleted", flush=True)
                
                # Set new webhook
                await telegram_app.bot.set_webhook(
                    url=webhook_url,
                    drop_pending_updates=False,
                    allowed_updates=None  # Allow all updates
                )
                logger.info(f"✅ Webhook set to {webhook_url}")
                print(f"✅ Webhook set to {webhook_url}", flush=True)
                
                # Verify webhook was set
                webhook_info = await telegram_app.bot.get_webhook_info()
                logger.info(f"✅ Webhook verified: {webhook_info.url}")
                print(f"✅ Webhook verified: {webhook_info.url}", flush=True)
                
            except Exception as webhook_error:
                logger.warning(f"⚠️ Failed to set webhook: {repr(webhook_error)}")
                print(f"⚠️ Failed to set webhook: {repr(webhook_error)}", flush=True)
        else:
            logger.warning("⚠️ BOT_WEBHOOK_URL is not set; skipping set_webhook")
            print("⚠️ BOT_WEBHOOK_URL is not set; skipping set_webhook", flush=True)
    except Exception as e:
        logger.error(f"❌ Failed to initialize Telegram bot: {repr(e)}", exc_info=True)
        print(f"❌ Failed to initialize Telegram bot: {repr(e)}", flush=True)
        # Don't raise - allow server to start even if bot initialization fails

    # Start background notification scheduler
    try:
        logger.info("📬 Starting notification scheduler...")
        print("📬 Starting notification scheduler...", flush=True)
        app.state.notification_scheduler_task = asyncio.create_task(
            NotificationScheduler.start_notification_scheduler()
        )
        logger.info("✅ Notification scheduler started")
        print("✅ Notification scheduler started", flush=True)
    except Exception as e:
        logger.error(f"❌ Failed to start notification scheduler: {repr(e)}", exc_info=True)
        print(f"❌ Failed to start notification scheduler: {repr(e)}", flush=True)
    
    logger.info("✅ Server startup completed successfully")
    print("✅ Server startup completed successfully", flush=True)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Shutdown logic for unified server."""
    # Stop background scheduler
    task = getattr(app.state, "notification_scheduler_task", None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    # Stop Telegram bot
    await telegram_app.stop()
    await telegram_app.shutdown()


@app.get("/")
async def health_check() -> dict:
    """Health check endpoint."""
    from database.connection import Database
    db_connected = await Database.is_connected()
    return {
        "status": "ok",
        "service": "Educational Platform",
        "bot_webhook": True,
        "admin_dashboard": True,
        "database": "connected" if db_connected else "disconnected",
    }


@app.get("/webhook/test")
async def webhook_test() -> dict:
    """Test webhook endpoint."""
    try:
        webhook_info = await telegram_app.bot.get_webhook_info()
        return {
            "status": "ok",
            "message": "Webhook endpoint is working",
            "webhook_url": BOT_WEBHOOK_URL,
            "telegram_webhook_info": {
                "url": webhook_info.url,
                "has_custom_certificate": webhook_info.has_custom_certificate,
                "pending_update_count": webhook_info.pending_update_count,
                "ip_address": webhook_info.ip_address,
                "last_error_date": webhook_info.last_error_date,
                "last_error_message": webhook_info.last_error_message,
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/webhook/test")
async def webhook_test_post(request: Request) -> dict:
    """Test webhook with POST request."""
    try:
        data = await request.json()
        logger.info(f"🧪 TEST WEBHOOK RECEIVED: {data}")
        print(f"🧪 TEST WEBHOOK RECEIVED: {data}", flush=True)
        
        # Try to process as update
        update = Update.de_json(data, telegram_app.bot)
        logger.info(f"🧪 TEST UPDATE CREATED: {update}")
        print(f"🧪 TEST UPDATE CREATED: {update}", flush=True)
        
        await telegram_app.process_update(update)
        logger.info(f"🧪 TEST UPDATE PROCESSED")
        print(f"🧪 TEST UPDATE PROCESSED", flush=True)
        
        return {"status": "ok", "message": "Test webhook processed successfully"}
    except Exception as e:
        logger.error(f"🧪 TEST WEBHOOK ERROR: {repr(e)}", exc_info=True)
        print(f"🧪 TEST WEBHOOK ERROR: {repr(e)}", flush=True)
        return {"status": "error", "message": str(e)}


@app.get("/health/db")
async def db_health_check() -> dict:
    """Database health check endpoint for monitoring."""
    from database.connection import Database
    try:
        is_connected = await Database.is_connected()
        if is_connected:
            return {
                "status": "healthy",
                "database": "MongoDB",
                "connected": True,
            }
        else:
            return {
                "status": "unhealthy",
                "database": "MongoDB",
                "connected": False,
                "error": "Database not initialized",
            }
    except Exception as e:
        logger.error(f"Database health check failed: {repr(e)}")
        return {
            "status": "unhealthy",
            "database": "MongoDB",
            "connected": False,
            "error": str(e),
        }


@app.post("/webhook")
@app.post("/api/webhook")
async def telegram_webhook(request: Request) -> dict:
    """Telegram webhook endpoint."""
    try:
        data = await request.json()
        logger.info(f"📨 Webhook received data: {data}")
        print(f"📨 Webhook received data: {data}", flush=True)
        
        # Check if it's a valid update
        if not data:
            logger.warning("⚠️ Empty webhook data received")
            print("⚠️ Empty webhook data received", flush=True)
            return {"ok": True}
        
        # Log update type
        if "message" in data:
            print(f"📨 Message received: {data['message']}", flush=True)
        if "callback_query" in data:
            print(f"📨 Callback query received: {data['callback_query']}", flush=True)
        
        update = Update.de_json(data, telegram_app.bot)
        logger.info(f"✅ Update created from data")
        print(f"✅ Update created: type={type(update)}, update_id={update.update_id}", flush=True)
        
        # Process the update
        logger.info(f"🔄 Processing update {update.update_id}...")
        print(f"🔄 Processing update {update.update_id}...", flush=True)
        
        await telegram_app.process_update(update)
        
        logger.info(f"✅ Update {update.update_id} processed successfully")
        print(f"✅ Update {update.update_id} processed successfully", flush=True)
        
        return {"ok": True}
    except Exception as e:
        # Log to both logger and stdout for Vercel visibility
        logger.error(f"❌ Webhook processing error: {repr(e)}", exc_info=True)
        print(f"❌ ERROR: Webhook processing failed: {repr(e)}", flush=True)
        import traceback
        traceback.print_exc()
        # Return 200 OK to Telegram (so it doesn't retry)
        # but log the error for debugging
        return {"ok": True, "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run("server:app", host=settings.HOST, port=port, reload=settings.DEBUG)
