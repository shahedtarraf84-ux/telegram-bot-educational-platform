# ✅ Deployment Checklist

## Pre-Deployment (Local)

- [ ] All files saved
- [ ] No syntax errors in Python files
- [ ] Dockerfile builds successfully locally
- [ ] entrypoint.sh has execute permissions

## Railway Configuration

### Environment Variables
- [ ] `TELEGRAM_BOT_TOKEN` - Set and valid
- [ ] `MONGODB_URL` - Set and accessible
- [ ] `MONGODB_DB_NAME` - Set (default: educational_platform)
- [ ] `BOT_WEBHOOK_URL` - Set to Railway domain + /webhook
- [ ] `TELEGRAM_ADMIN_ID` - Set to your admin ID
- [ ] `SECRET_KEY` - Set to a secure random string
- [ ] `ADMIN_PASSWORD` - Set to a secure password
- [ ] `ADMIN_EMAIL` - Set to admin email
- [ ] `SHAP_CASH_NUMBER` - Set to payment number
- [ ] `HARAM_NUMBER` - Set to payment number

### Port Configuration
- [ ] Railway PORT variable is NOT manually set (Railway sets it automatically)
- [ ] Dockerfile uses `${PORT:-8080}` syntax
- [ ] entrypoint.sh exists and is executable

## Deployment Steps

1. **Commit and Push**
   ```bash
   git add .
   git commit -m "Fix: Critical PORT environment variable handling"
   git push origin main
   ```

2. **Monitor Railway**
   - [ ] Build starts automatically
   - [ ] Build completes without errors
   - [ ] Deployment starts
   - [ ] Container starts successfully

3. **Check Logs**
   - [ ] No "Invalid value for '--port'" errors
   - [ ] See "Starting Educational Platform server..."
   - [ ] See "MongoDB connection established"
   - [ ] See "Telegram bot initialized"
   - [ ] See "Webhook set to..."

## Post-Deployment Testing

1. **Health Check**
   ```
   GET https://your-railway-domain.railway.app/
   Expected: {"status": "ok", "service": "Educational Platform", ...}
   ```

2. **Database Health**
   ```
   GET https://your-railway-domain.railway.app/health/db
   Expected: {"status": "healthy", "database": "MongoDB", "connected": true}
   ```

3. **Telegram Bot**
   - [ ] Send `/start` to bot
   - [ ] Receive welcome message
   - [ ] Bot responds to commands

4. **Admin Dashboard**
   - [ ] Access https://your-railway-domain.railway.app/admin
   - [ ] Login with admin credentials
   - [ ] Dashboard loads without errors

## Troubleshooting

### Build Fails
- [ ] Check Python syntax
- [ ] Verify requirements.txt has all dependencies
- [ ] Check Dockerfile for typos

### Container Won't Start
- [ ] Check logs for startup errors
- [ ] Verify all required environment variables are set
- [ ] Check MongoDB connection string

### Bot Not Responding
- [ ] Verify TELEGRAM_BOT_TOKEN is correct
- [ ] Check BOT_WEBHOOK_URL matches Railway domain
- [ ] Verify webhook is set in logs

### Database Connection Fails
- [ ] Check MONGODB_URL is correct
- [ ] Verify MongoDB Atlas IP whitelist
- [ ] Check network connectivity

## Rollback Plan

If deployment fails:
1. Check logs for specific error
2. Fix the issue locally
3. Commit and push
4. Railway will auto-redeploy

---

**Last Updated**: 2025-12-01
**Status**: Ready for deployment
