import os

from fastapi import FastAPI, Request
from loguru import logger
from telegram import Update

from bot.main import create_application
from config.settings import settings


telegram_app = create_application()
app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    await telegram_app.initialize()
    await telegram_app.start()

    webhook_url = settings.BOT_WEBHOOK_URL
    if webhook_url:
        await telegram_app.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    else:
        logger.warning("BOT_WEBHOOK_URL is not set; skipping set_webhook")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await telegram_app.stop()
    await telegram_app.shutdown()


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run("webhook_server:app", host=settings.HOST, port=port)
