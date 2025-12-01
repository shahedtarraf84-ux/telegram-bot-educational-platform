# 🔴 CRITICAL FIX GUIDE - Bot Startup Issues

## Problem Summary
The bot was crashing on Railway with:
```
ERROR: Invalid value for '--port': '$PORT' is not a valid integer.
```

## Root Causes Fixed

### 1. ✅ Dockerfile CMD Issue
**Problem**: The `$PORT` environment variable wasn't being expanded properly
```dockerfile
# ❌ WRONG - Shell variables not expanded in exec form
CMD python -m uvicorn server:app --host 0.0.0.0 --port $PORT
```

**Solution**: Use shell form with proper variable expansion
```dockerfile
# ✅ CORRECT - Shell form with variable expansion
CMD ["sh", "-c", "python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}"]
```

### 2. ✅ Entrypoint Script
Created `/entrypoint.sh` to handle startup more robustly:
- Proper shell variable expansion
- Debug logging for troubleshooting
- Fallback to port 8080 if PORT not set

### 3. ✅ Server Startup Resilience
Modified `server.py` startup logic:
- Database connection failures no longer crash the server
- Bot initialization failures don't prevent server startup
- Webhook setup failures are handled gracefully
- Server continues with partial functionality if needed

## Files Modified

### 1. `Dockerfile`
- Changed CMD to use shell form with proper variable expansion
- Added entrypoint script
- Made script executable with chmod

### 2. `entrypoint.sh` (NEW)
- Handles PORT environment variable properly
- Provides debug logging
- Ensures proper startup sequence

### 3. `server.py`
- Removed `raise` statements from startup exceptions
- Added graceful degradation
- Better error logging

## Deployment Steps

### Step 1: Verify Environment Variables on Railway
Make sure these are set in Railway dashboard:
```
TELEGRAM_BOT_TOKEN=your_token_here
MONGODB_URL=your_mongodb_url
MONGODB_DB_NAME=educational_platform
BOT_WEBHOOK_URL=https://your-railway-domain.railway.app/webhook
TELEGRAM_ADMIN_ID=your_admin_id
SECRET_KEY=your_secret_key
ADMIN_PASSWORD=your_admin_password
ADMIN_EMAIL=admin@example.com
SHAP_CASH_NUMBER=your_number
HARAM_NUMBER=your_number
```

### Step 2: Redeploy to Railway
```bash
# Push changes to GitHub
git add .
git commit -m "Fix: Critical PORT environment variable handling in Docker"
git push

# Railway will auto-redeploy from GitHub
```

### Step 3: Monitor Logs
Check Railway logs for:
- ✅ "Starting Educational Platform server..."
- ✅ "MongoDB connection established"
- ✅ "Telegram bot initialized"
- ✅ "Webhook set to..."

## Testing Locally (Optional)

### Test with Docker
```bash
# Build image
docker build -t edu-bot .

# Run with PORT environment variable
docker run -e PORT=8080 \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e MONGODB_URL=your_url \
  -e MONGODB_DB_NAME=educational_platform \
  -e BOT_WEBHOOK_URL=http://localhost:8080/webhook \
  -e TELEGRAM_ADMIN_ID=your_id \
  -e SECRET_KEY=secret \
  -e ADMIN_PASSWORD=password \
  -e ADMIN_EMAIL=admin@example.com \
  -e SHAP_CASH_NUMBER=number \
  -e HARAM_NUMBER=number \
  edu-bot
```

### Test with Python directly
```bash
# Set environment variables
export PORT=8080
export TELEGRAM_BOT_TOKEN=your_token
# ... set other variables

# Run
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

## Troubleshooting

### Issue: Still seeing PORT errors
**Solution**: 
1. Clear Railway build cache
2. Force redeploy
3. Check that entrypoint.sh is in the Docker image

### Issue: Bot not responding to /start
**Solution**:
1. Check BOT_WEBHOOK_URL is correct
2. Verify TELEGRAM_BOT_TOKEN is valid
3. Check MongoDB connection in logs

### Issue: Database connection fails
**Solution**:
1. Verify MONGODB_URL is correct
2. Check MongoDB Atlas IP whitelist includes Railway
3. Verify MONGODB_DB_NAME matches your database

## What Changed

| File | Change | Impact |
|------|--------|--------|
| Dockerfile | CMD → shell form with variable expansion | Fixes PORT parsing |
| entrypoint.sh | NEW - startup script | Robust startup handling |
| server.py | Removed raise on startup errors | Server stays up even with partial failures |

## Next Steps

1. ✅ Push changes to GitHub
2. ✅ Railway auto-redeploys
3. ✅ Monitor logs for success
4. ✅ Test /start command in Telegram
5. ✅ Verify admin dashboard works

---

**Status**: 🟢 Ready for deployment
**Last Updated**: 2025-12-01
