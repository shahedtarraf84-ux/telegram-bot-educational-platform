#!/bin/bash
set -e

# Get the port from environment variable, default to 8000
PORT=${PORT:-8000}

# Run the application
python -m uvicorn server:app --host 0.0.0.0 --port $PORT
