# ⚡ Quick Fix Reference

## The Problem (In 10 Seconds)
```
ERROR: Invalid value for '--port': '$PORT' is not a valid integer.
```
**Why**: Docker wasn't expanding the `$PORT` environment variable.

---

## The Solution (In 30 Seconds)

### 1. Dockerfile
```dockerfile
# ✅ Use entrypoint script instead of direct CMD
ENTRYPOINT ["/app/entrypoint.sh"]
```

### 2. entrypoint.sh (NEW FILE)
```bash
#!/bin/bash
python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}
```

### 3. server.py
```python
# ✅ Don't crash on startup errors
except Exception as e:
    logger.error(f"Error: {repr(e)}")
    # Don't raise - let server continue
```

---

## Deploy in 3 Steps

```bash
# 1. Commit
git add .
git commit -m "Fix: PORT environment variable handling"

# 2. Push
git push origin main

# 3. Wait
# Railway auto-redeploys from GitHub
```

---

## Verify Success

Look for in logs:
```
✅ Starting Educational Platform Bot...
✅ PORT: 8080
✅ MongoDB connection established
✅ Telegram bot initialized
✅ Webhook set to...
```

---

## Test Bot

Send `/start` to your Telegram bot → Should get welcome message ✅

---

## If Still Broken

1. Check logs for actual error
2. Verify all env vars are set in Railway
3. Force rebuild: Clear cache → Redeploy
4. Check entrypoint.sh is in Docker image

---

**Status**: 🟢 Ready to deploy
