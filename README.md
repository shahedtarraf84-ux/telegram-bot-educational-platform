# Telegram Bot Educational Platform

منصة تعليمية متكاملة مبنية على **Telegram Bot** مع لوحة تحكم **FastAPI** وقاعدة بيانات **MongoDB/Beanie**.

## المتطلبات

- Python 3.10+
- MongoDB (محلي أو MongoDB Atlas)
- حساب Telegram Bot Token

## التثبيت المحلي

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## تشغيل البوت محلياً

```bash
venv\Scripts\activate
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

- التطبيق يعمل على: `http://localhost:8000`
- صفحة التوثيق (Swagger): `http://localhost:8000/docs`
- لوحة التحكم: `http://localhost:8000/admin`

## النشر على Railway

### الطريقة السريعة

1. **ادفع الكود إلى GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **اذهب إلى [railway.app](https://railway.app)**
   - انقر على "New Project"
   - اختر "Deploy from GitHub"
   - اختر مستودعك

3. **أضف متغيرات البيئة**
   - في Railway dashboard، انقر على "Variables"
   - أضف جميع المتغيرات من `.env.railway`

4. **حدّث webhook الـ Telegram**
   ```bash
   curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
     -d url=https://your-app-name.up.railway.app/webhook
   ```

### الدليل الكامل

انظر [RAILWAY_DEPLOYMENT_GUIDE.md](./RAILWAY_DEPLOYMENT_GUIDE.md) للتفاصيل الكاملة.

### قائمة التحقق

انظر [RAILWAY_SETUP_CHECKLIST.md](./RAILWAY_SETUP_CHECKLIST.md) للخطوات خطوة بخطوة.

### الأوامر المفيدة

انظر [RAILWAY_COMMANDS.md](./RAILWAY_COMMANDS.md) لقائمة الأوامر.

## المتغيرات الحساسة

- ملف `.env` يحتوي على:
  - `TELEGRAM_BOT_TOKEN`
  - `MONGODB_URL`
  - `SECRET_KEY`
  - إعدادات أخرى حساسة

- ملف `.env.railway` يحتوي على قالب جميع المتغيرات المطلوبة على Railway

> **مهم:** ملف `.env` مُستثنى في `.gitignore` ولن يتم رفعه إلى GitHub.

## الملفات المضافة للنشر على Railway

- `Dockerfile` - تعريف الحاوية
- `Procfile` - أمر التشغيل
- `railway.json` و `railway.yaml` - إعدادات Railway
- `.dockerignore` - الملفات المستثناة من Docker
- `.env.railway` - قالب المتغيرات

## المميزات

✅ Telegram Bot مع webhook support
✅ لوحة تحكم إدارية
✅ قاعدة بيانات MongoDB
✅ جدولة إشعارات خلفية
✅ نظام الامتحانات والواجبات
✅ إدارة المستخدمين
✅ دعم الملفات والصور

## الدعم والمساعدة

- [توثيق Railway](https://docs.railway.app)
- [توثيق FastAPI](https://fastapi.tiangolo.com)
- [توثيق Python Telegram Bot](https://python-telegram-bot.readthedocs.io)
