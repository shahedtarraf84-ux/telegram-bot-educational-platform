"""
Hybrid Server - FastAPI + Telegram Bot Polling
This runs both FastAPI server and Telegram bot in polling mode.
Version: 2.0 - With webhook endpoint support
"""

import os
import asyncio
import uvicorn
from loguru import logger
from fastapi import FastAPI, Request
from telegram import Update

from config.settings import settings
from bot.main import create_application
from database.connection import Database

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or settings.TELEGRAM_BOT_TOKEN
MONGODB_URL = os.environ.get("MONGODB_URL") or settings.MONGODB_URL
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME") or settings.MONGODB_DB_NAME

# Create FastAPI app
app = FastAPI(title="Educational Platform - Polling Mode")

# Global telegram app
telegram_app = None
polling_task = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "service": "Educational Platform",
        "mode": "polling",
        "message": "Bot is running in polling mode"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.post("/webhook")
@app.post("/api/webhook")
async def telegram_webhook(request: Request) -> dict:
    """Telegram webhook endpoint - for compatibility"""
    try:
        data = await request.json()
        logger.info(f"📨 Webhook received data: {data}")
        print(f"📨 Webhook received data: {data}", flush=True)
        
        if not data:
            logger.warning("⚠️ Empty webhook data received")
            print("⚠️ Empty webhook data received", flush=True)
            return {"ok": True}
        
        # Log update type
        if "message" in data:
            print(f"📨 Message received: {data['message']}", flush=True)
        if "callback_query" in data:
            print(f"📨 Callback query received: {data['callback_query']}", flush=True)
        
        if telegram_app:
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
        logger.error(f"❌ Webhook processing error: {repr(e)}", exc_info=True)
        print(f"❌ ERROR: Webhook processing failed: {repr(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return {"ok": True, "error": str(e)}


@app.on_event("startup")
async def startup():
    """Startup event"""
    global telegram_app, polling_task
    
    logger.info("🚀 Starting Educational Platform Server in POLLING MODE...")
    print("🚀 Starting Educational Platform Server in POLLING MODE...", flush=True)
    
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
        
        # Start polling in background
        logger.info("🔄 Starting polling mode...")
        print("🔄 Starting polling mode...", flush=True)
        
        async def run_polling():
            try:
                await telegram_app.run_polling(
                    allowed_updates=None,
                    drop_pending_updates=False,
                    close_loop=False
                )
            except Exception as e:
                logger.error(f"❌ Polling error: {repr(e)}", exc_info=True)
                print(f"❌ Polling error: {repr(e)}", flush=True)
        
        polling_task = asyncio.create_task(run_polling())
        
        print("✅ Bot is now running in POLLING MODE", flush=True)
        print("✅ Bot will receive messages via polling", flush=True)
        logger.info("✅ Server startup completed successfully")
        print("✅ Server startup completed successfully", flush=True)
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {repr(e)}", exc_info=True)
        print(f"❌ Failed to start bot: {repr(e)}", flush=True)


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event"""
    global telegram_app, polling_task
    
    logger.info("🛑 Shutting down server...")
    print("🛑 Shutting down server...", flush=True)
    
    if polling_task:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    
    if telegram_app:
        try:
            await telegram_app.stop()
            await telegram_app.shutdown()
        except:
            pass


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("polling_server:app", host="0.0.0.0", port=port, reload=False)
