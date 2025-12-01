#!/bin/bash
set -e

echo "🚀 Starting Educational Platform Bot..."
echo "PORT: ${PORT:-8080}"
echo "TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:0:10}..."
echo "MONGODB_URL: ${MONGODB_URL:0:30}..."

exec python polling_server.py
