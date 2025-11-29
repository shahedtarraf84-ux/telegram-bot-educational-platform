# 🔧 Debugging Guide - Educational Platform

## Critical Issues Fixed

### 1. **Database Connection Failures** ✅
**Problem**: MongoDB connection was failing silently without retry logic
**Solution**: Added retry mechanism with 3 attempts and 2-second delays
- File: `database/connection.py`
- Added connection timeout settings (5s server selection, 10s connect, 10s socket)
- Added ping test to verify connection before initializing Beanie
- Detailed logging at each retry attempt

### 2. **Generic Error Messages** ✅
**Problem**: Users saw "❌ حدث خطأ" without knowing the actual error
**Solution**: Added detailed error logging to all database operations
- Files: `bot/handlers/courses.py`, `bot/handlers/materials.py`, `bot/handlers/content.py`
- Now logs actual database errors to console/logs
- Users still see friendly messages, but admins can see real errors in logs

### 3. **Admin Dashboard Crashes** ✅
**Problem**: Dashboard crashed when fetching statistics
**Solution**: Added try-catch blocks with fallback values
- File: `admin_dashboard/app.py`
- Dashboard returns partial data if some queries fail
- All database errors are logged with full details

### 4. **Missing Error Handling in Handlers** ✅
**Problem**: Course and material handlers didn't catch database errors
**Solution**: Wrapped all database queries in try-catch blocks
- Added nested error handling for database operations
- Proper error messages sent to users
- Full error details logged for debugging

---

## 🚀 How to Debug Issues

### Step 1: Check MongoDB Connection
```bash
# Test if MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Or use MongoDB Compass to connect
# Connection string: mongodb://username:password@host:port/database
```

### Step 2: Check Environment Variables
Verify your `.env` file contains all required variables:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_ADMIN_ID=your_admin_id
MONGODB_URL=mongodb://user:pass@host:port
MONGODB_DB_NAME=educational_platform
SECRET_KEY=your_secret_key
ADMIN_PASSWORD=your_password
ADMIN_EMAIL=admin@example.com
SHAP_CASH_NUMBER=your_number
HARAM_NUMBER=your_number
```

### Step 3: Check Server Logs
When running the bot, look for these log messages:

**✅ Success Indicators:**
```
[Attempt 1/3] Connecting to MongoDB: mongodb://***:***@host:port, db=educational_platform
✅ MongoDB ping successful
✅ MongoDB connected successfully and Beanie initialized
```

**❌ Error Indicators:**
```
❌ [Attempt 1/3] MongoDB connection failed: Connection refused
❌ Max retries reached. Could not connect to MongoDB.
```

### Step 4: Test Each Component

#### Test MongoDB Connection
```bash
python test_mongodb.py
```

#### Test Bot Connection
```bash
python test_bot_connection.py
```

#### Test Complete System
```bash
python test_complete_system.py
```

---

## 📋 Common Issues and Solutions

### Issue 1: "Connection Refused"
**Cause**: MongoDB is not running or not accessible
**Solution**:
1. Start MongoDB: `mongod` or `docker-compose up -d` (if using Docker)
2. Verify connection string in `.env`
3. Check firewall/network access to MongoDB host

### Issue 2: "Authentication Failed"
**Cause**: Wrong username/password in MongoDB URL
**Solution**:
1. Verify credentials in `.env`
2. Check MongoDB user permissions
3. Ensure user has access to the database

### Issue 3: "Database Not Found"
**Cause**: Database name mismatch
**Solution**:
1. Verify `MONGODB_DB_NAME` in `.env` matches your database
2. Create database if it doesn't exist: `use educational_platform`

### Issue 4: "Timeout"
**Cause**: MongoDB server is slow or unreachable
**Solution**:
1. Check MongoDB server status
2. Increase timeout values in `database/connection.py` if needed
3. Check network connectivity

### Issue 5: "Admin Dashboard Not Opening"
**Cause**: Dashboard server not running or database connection failed
**Solution**:
1. Check if server is running: `python server.py`
2. Check logs for database connection errors
3. Verify admin credentials in `.env`

---

## 🔍 Detailed Error Logging

All errors are now logged with full details. Check logs for:

### Bot Errors
Look for lines like:
```
❌ [Attempt 2/3] MongoDB connection failed: Connection refused
Database error while fetching user 123456789: [error details]
Error in show_course_details: [error details]
```

### Dashboard Errors
Look for lines like:
```
Dashboard error: [error details]
Students list error: [error details]
Error fetching pending approvals: [error details]
```

---

## 📊 Testing Checklist

- [ ] MongoDB is running and accessible
- [ ] `.env` file has all required variables
- [ ] Bot can connect to MongoDB (check logs for "✅ MongoDB connected")
- [ ] Admin can see dashboard (no 500 errors)
- [ ] Admin can view subjects (no "❌ حدث خطأ")
- [ ] Admin can view courses (no "❌ حدث خطأ")
- [ ] Admin can view stats (no "❌ حدث خطأ في عرض الإحصائيات")
- [ ] Student registration works (can save email without error)
- [ ] Student can view courses after registration
- [ ] Payment flow works (can submit payment proof)

---

## 🛠️ Quick Fixes

### If Bot Won't Start
1. Check MongoDB is running
2. Check `.env` file exists and has `TELEGRAM_BOT_TOKEN`
3. Check logs for connection errors
4. Run `python test_mongodb.py` to test database

### If Dashboard Won't Open
1. Check server is running: `python server.py`
2. Check admin credentials in `.env`
3. Check logs for database errors
4. Try accessing `http://localhost:8000/` directly

### If Database Queries Fail
1. Check MongoDB connection (see Step 1)
2. Check `.env` variables (see Step 2)
3. Check logs for detailed error messages (see Step 3)
4. Run test scripts (see Step 4)

---

## 📝 Log Levels

The system uses `loguru` for logging. Log levels are:
- **INFO**: Normal operations (connection successful, user registered, etc.)
- **DEBUG**: Detailed information (query parameters, user data, etc.)
- **ERROR**: Errors that need attention (connection failed, database error, etc.)

To see DEBUG logs, set in your code:
```python
from loguru import logger
logger.enable("__main__")  # Enable all logs
```

---

## 🎯 Next Steps

1. **Verify MongoDB Connection**: Run `test_mongodb.py`
2. **Check Environment Variables**: Review `.env` file
3. **Start the Server**: Run `python server.py`
4. **Monitor Logs**: Watch for error messages
5. **Test Each Feature**: Use the testing checklist above

If you still have issues, check the logs for detailed error messages and share them for further debugging.
