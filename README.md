# IX SPX Bot — V1

هذه النسخة تشغّل واجهة البوت والقائمة الرئيسية فقط.
لا تحتوي على إشارات تداول حقيقية بعد.

## متغيرات البيئة
- BOT_TOKEN: توكن بوت تيليجرام (ضعه في Secrets/Environment Variables فقط)
- WEBHOOK_URL: رابط خدمة Render مثل https://ix-spx-bot.onrender.com

## التشغيل
Build: pip install -r requirements.txt
Start: gunicorn main:app --bind 0.0.0.0:$PORT

بعد تشغيل الخدمة، افتح البوت وأرسل /start.
