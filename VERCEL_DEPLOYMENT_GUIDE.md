# دليل نشر Dashboard على Vercel

**Status:** ✅ **تم إصلاح vercel.json**

---

## 🎯 الخطوات الأساسية للنشر:

### 1. **تأكد من الملفات:**

✅ `vercel.json` - تم تحديثه
✅ `requirements.txt` - موجود
✅ `server.py` - يحتوي على Dashboard
✅ `admin_dashboard/app.py` - Dashboard FastAPI

---

### 2. **أضف متغيرات البيئة في Vercel:**

اذهب إلى: **Vercel Dashboard → Project Settings → Environment Variables**

أضف المتغيرات التالية:

```
MONGODB_URL = mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME = educational_platform
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_ADMIN_ID = your_admin_id
BOT_WEBHOOK_URL = https://your-app.vercel.app/api/webhook
ADMIN_USERNAME = admin
ADMIN_PASSWORD = your_admin_password
ADMIN_EMAIL = admin@example.com
SECRET_KEY = your_secret_key
SHAP_CASH_NUMBER = your_number
HARAM_NUMBER = your_number
```

---

### 3. **أعد النشر:**

```bash
# تأكد من أنك في المجلد الصحيح
cd d:\bot_telegram\Educational_Platform

# أعد النشر
vercel deploy --prod
```

---

### 4. **الوصول إلى Dashboard:**

بعد النشر الناجح، استخدم:

```
https://your-app.vercel.app/admin
```

**بيانات الدخول:**
- Username: `admin`
- Password: (كما حددت في ADMIN_PASSWORD)

---

## 📋 ملف vercel.json المحدث:

```json
{
  "version": 2,
  "buildCommand": "pip install -r requirements.txt",
  "builds": [
    { "src": "server.py", "use": "@vercel/python" },
    { "src": "api/*.py", "use": "@vercel/python" }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1.py"
    },
    {
      "src": "/(.*)",
      "dest": "/server.py"
    }
  ],
  "env": {
    "MONGODB_URL": "@mongodb_url",
    "MONGODB_DB_NAME": "@mongodb_db_name",
    "TELEGRAM_BOT_TOKEN": "@telegram_bot_token",
    "TELEGRAM_ADMIN_ID": "@telegram_admin_id",
    "BOT_WEBHOOK_URL": "@bot_webhook_url"
  },
  "functions": {
    "server.py": {
      "memory": 3008,
      "maxDuration": 60
    },
    "api/webhook.py": {
      "memory": 3008,
      "maxDuration": 60
    }
  }
}
```

---

## 🔍 ماذا يحتوي Dashboard:

### الصفحات المتاحة:

1. **Dashboard الرئيسية** (`/admin`)
   - إجمالي المستخدمين
   - الموافقات المعلقة
   - آخر المستخدمين المسجلين

2. **قائمة الطلاب** (`/admin/students`)
   - جميع الطلاب المسجلين
   - معلومات التسجيل

3. **تفاصيل الطالب** (`/admin/student/{telegram_id}`)
   - معلومات الطالب الكاملة
   - الدورات المسجلة
   - التقدم الدراسي

4. **الإشعارات** (`/admin/notifications`)
   - إرسال إشعارات للطلاب

---

## ✅ المميزات:

✅ مصادقة HTTP Basic
✅ معالجة أخطاء شاملة
✅ تسجيل تفصيلي
✅ عرض بيانات من MongoDB
✅ واجهة ويب جميلة

---

## 🚀 للتشغيل محلياً:

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الخادم
python server.py

# افتح المتصفح على:
http://localhost:8000/admin
```

---

## ⚠️ إذا حدثت مشاكل:

### 1. **خطأ 404:**
- تأكد من أن `vercel.json` محدث
- أعد النشر: `vercel deploy --prod`

### 2. **خطأ 401 (غير مصرح):**
- تحقق من بيانات المسؤول
- استخدم ADMIN_USERNAME و ADMIN_PASSWORD الصحيحة

### 3. **خطأ في قاعدة البيانات:**
- تأكد من MONGODB_URL صحيح
- تحقق من أن قاعدة البيانات متصلة

### 4. **عرض السجلات:**
```bash
vercel logs
```

---

## 📝 ملخص:

| العنصر | الحالة |
|--------|--------|
| vercel.json | ✅ محدث |
| requirements.txt | ✅ موجود |
| server.py | ✅ يحتوي على Dashboard |
| admin_dashboard/app.py | ✅ جاهز |
| متغيرات البيئة | ⏳ تحتاج إلى إضافة |

---

## 🎉 النتيجة المتوقعة:

بعد اتباع هذه الخطوات، سيكون لديك:

✅ Dashboard يعمل على Vercel
✅ يمكن الوصول إليه من أي مكان
✅ يعرض بيانات المستخدمين من MongoDB
✅ واجهة آمنة مع مصادقة

**جاهز للإنتاج!** 🚀
