# 🔧 Technical Explanation - PORT Variable Issue

## The Problem Visualized

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAILWAY DEPLOYMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Railway Container Environment:                                │
│  ┌──────────────────────────────────┐                          │
│  │ PORT = 8080                      │                          │
│  │ TELEGRAM_BOT_TOKEN = abc123...   │                          │
│  │ MONGODB_URL = mongodb+srv://...  │                          │
│  └──────────────────────────────────┘                          │
│                    ↓                                            │
│  ❌ BEFORE (BROKEN):                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Dockerfile CMD (exec form):                              │  │
│  │ CMD python -m uvicorn server:app --port $PORT            │  │
│  │                                                          │  │
│  │ What Docker does:                                        │  │
│  │ 1. Exec form = NO shell spawned                          │  │
│  │ 2. Variables NOT expanded                                │  │
│  │ 3. Passes literal "$PORT" to uvicorn                     │  │
│  │                                                          │  │
│  │ uvicorn receives: "--port $PORT"                         │  │
│  │ uvicorn tries: int("$PORT")  ← FAILS!                   │  │
│  │ Error: Invalid value for '--port': '$PORT' is not a     │  │
│  │        valid integer.                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ✅ AFTER (FIXED):                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Dockerfile ENTRYPOINT:                                   │  │
│  │ ENTRYPOINT ["/app/entrypoint.sh"]                        │  │
│  │                                                          │  │
│  │ entrypoint.sh:                                           │  │
│  │ #!/bin/bash                                              │  │
│  │ python -m uvicorn server:app --port ${PORT:-8080}        │  │
│  │                                                          │  │
│  │ What Docker does:                                        │  │
│  │ 1. Runs shell script                                     │  │
│  │ 2. Shell expands ${PORT:-8080}                           │  │
│  │ 3. Passes actual port number to uvicorn                  │  │
│  │                                                          │  │
│  │ uvicorn receives: "--port 8080"                          │  │
│  │ uvicorn tries: int("8080")  ← SUCCESS!                  │  │
│  │ Server starts on port 8080 ✅                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Docker CMD vs ENTRYPOINT Explained

### Exec Form (No Shell)
```dockerfile
CMD ["python", "-m", "uvicorn", "server:app", "--port", "$PORT"]
```
- Docker runs: `python -m uvicorn server:app --port $PORT`
- **NO shell** = **NO variable expansion**
- `$PORT` passed as literal string

### Shell Form (With Shell)
```dockerfile
CMD python -m uvicorn server:app --port $PORT
```
- Docker runs: `/bin/sh -c "python -m uvicorn server:app --port $PORT"`
- **Has shell** = **Variables expanded**
- `$PORT` expanded to actual value

### Our Solution (Entrypoint Script)
```dockerfile
ENTRYPOINT ["/app/entrypoint.sh"]
```
- Docker runs: `/app/entrypoint.sh`
- Script is bash = **Variables expanded**
- `${PORT:-8080}` properly expanded with fallback

---

## Variable Expansion Syntax

### Bash Variable Expansion
```bash
# Simple expansion
${PORT}              # Expands to value of PORT

# With default value
${PORT:-8080}        # Use PORT if set, otherwise 8080

# With assignment
${PORT:=8080}        # Use PORT if set, otherwise set to 8080

# String operations
${PORT:0:5}          # First 5 characters
${PORT#prefix}       # Remove prefix
${PORT%suffix}       # Remove suffix
```

### Our entrypoint.sh
```bash
#!/bin/bash
python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}
```
- `${PORT:-8080}` means:
  - If `PORT` is set: use its value
  - If `PORT` is not set: use `8080`
  - Railway sets PORT, so it uses Railway's value
  - Local testing: falls back to 8080

---

## Startup Resilience Fix

### Before (Crashes on Error)
```python
@app.on_event("startup")
async def on_startup():
    try:
        await Database.connect()
    except Exception as e:
        logger.error(f"DB error: {e}")
        raise  # ❌ CRASHES SERVER
```

### After (Continues on Error)
```python
@app.on_event("startup")
async def on_startup():
    try:
        await Database.connect()
    except Exception as e:
        logger.error(f"DB error: {e}")
        # ✅ NO RAISE - server continues
        print("⚠️ Server continuing without database connection")
```

### Benefits
- Server stays up even if DB fails initially
- Webhook still works for incoming messages
- Can retry DB connection later
- Better user experience (partial service vs complete failure)

---

## Complete Startup Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   RAILWAY CONTAINER START                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  1. Docker reads ENTRYPOINT ["/app/entrypoint.sh"]          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. entrypoint.sh runs in bash shell                        │
│     - Expands ${PORT:-8080} to 8080                         │
│     - Runs: python -m uvicorn server:app --port 8080        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. uvicorn starts FastAPI app                              │
│     - Listens on 0.0.0.0:8080                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. FastAPI startup events trigger                          │
│     - Try: Connect to MongoDB                               │
│     - Try: Initialize Telegram bot                          │
│     - Try: Start notification scheduler                     │
│     - If any fail: Log error but continue                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Server ready to accept requests                         │
│     - Health check: GET /                                   │
│     - Webhook: POST /webhook                                │
│     - Admin: /admin                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Environment Variable Resolution

```
┌─────────────────────────────────────────────────────────────┐
│           HOW PORT VARIABLE IS RESOLVED                     │
└─────────────────────────────────────────────────────────────┘

Railway Container:
  PORT = 8080 (set by Railway)

entrypoint.sh execution:
  ${PORT:-8080}
    ↓
  Check: Is PORT set?
    ↓
  YES → Use PORT value
    ↓
  Result: 8080

Command executed:
  python -m uvicorn server:app --port 8080

Local testing (if PORT not set):
  ${PORT:-8080}
    ↓
  Check: Is PORT set?
    ↓
  NO → Use default value
    ↓
  Result: 8080

Command executed:
  python -m uvicorn server:app --port 8080
```

---

## Why This Matters

| Aspect | Before | After |
|--------|--------|-------|
| **Port Handling** | Literal "$PORT" string | Actual port number (8080) |
| **Startup Errors** | Server crashes | Server continues |
| **Error Visibility** | Complete failure | Partial functionality |
| **Debugging** | Hard to trace | Clear error logs |
| **Resilience** | Fragile | Robust |

---

## Summary

The fix addresses two critical issues:

1. **Docker Variable Expansion**
   - Problem: Exec form doesn't expand variables
   - Solution: Use shell script with proper expansion
   - Result: PORT properly passed to uvicorn

2. **Startup Resilience**
   - Problem: Any error crashes the server
   - Solution: Graceful error handling
   - Result: Server stays up with partial functionality

This ensures your bot:
- ✅ Starts without PORT errors
- ✅ Continues running even if DB fails initially
- ✅ Provides better error visibility
- ✅ Handles edge cases gracefully

---

**Technical Level**: Intermediate
**Impact**: Critical - Fixes production deployment
**Status**: ✅ Implemented and tested
