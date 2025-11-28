"""FastAPI entrypoint for Vercel / generic deployments.
This file simply re-exports the Telegram bot webhook FastAPI app
so that platforms looking for main.app can find the webhook server.
"""

from webhook_server import app  # noqa: F401
