# 🤖 بوت العروض الذكي

بوت تيليجرام يراقب قنوات العروض تلقائياً، يصنفها بـ Claude AI، ويرسلها لقناتك الخاصة.

---

## ⚡ التشغيل في 5 خطوات

### الخطوة ١ — احصل على بيانات تيليجرام

**أ. API ID و Hash:**
1. افتح [my.telegram.org](https://my.telegram.org)
2. سجّل دخول برقم هاتفك
3. اختر **API development tools**
4. أنشئ تطبيق — احفظ `api_id` و `api_hash`

**ب. Bot Token:**
1. كلّم [@BotFather](https://t.me/BotFather) في تيليجرام
2. اكتب `/newbot`
3. سمّي البوت واحفظ الـ **Token**

**ج. أضف البوت للقنوات:**
- في كل قناة مصدر: Settings → Administrators → Add Admin
- أضف بوتك بصلاحية **Post Messages** فقط

### الخطوة ٢ — احصل على Anthropic API Key

1. افتح [console.anthropic.com](https://console.anthropic.com)
2. API Keys → Create Key
3. احفظ المفتاح

### الخطوة ٣ — اعمل قناة وجهة

1. أنشئ قناة خاصة جديدة في تيليجرام
2. أضف البوت كـ Admin بصلاحية النشر
3. احفظ الـ username (مثال: `@my_deals_bot`)

### الخطوة ٤ — اضبط الإعدادات

```bash
# انسخ ملف الإعدادات
cp .env.example .env

# افتح وعدّل القيم
nano .env
```

أهم القيم:
```
SOURCE_CHANNELS=@قناة1,@قناة2,@قناة3
DEST_CHANNEL=@قناتك_الخاصة
MIN_DISCOUNT=15
```

### الخطوة ٥ — شغّل البوت

**محلياً (للاختبار):**
```bash
pip install -r requirements.txt
python bot.py
```

**على Railway (مجاناً - للتشغيل الدائم):**
```bash
# ١. ارفع الملفات على GitHub
# ٢. افتح railway.app
# ٣. New Project → Deploy from GitHub
# ٤. أضف المتغيرات في Variables tab
# ٥. Deploy!
```

---

## 📦 هيكل الملفات

```
deals_bot/
├── bot.py              ← الكود الرئيسي
├── requirements.txt    ← المكتبات
├── railway.toml        ← إعدادات الرفع
├── .env.example        ← نموذج الإعدادات
└── .env                ← إعداداتك (لا ترفعه!)
```

---

## 🎛️ تخصيص البوت

### تغيير شكل الرسالة
في `bot.py` → دالة `format_deal_message()` — عدّل النص والإيموجي

### إضافة فلترة بالمتجر
```python
# في handle_new_message أضف:
if deal.get("store") not in ["amazon", "noon"]:
    return  # تجاهل الجوميا مثلاً
```

### فلترة بالفئة
```python
allowed_categories = ["إلكترونيات", "أجهزة منزلية"]
if deal.get("category") not in allowed_categories:
    return
```

### إرسال لأكثر من قناة
```python
# إرسال الإلكترونيات لقناة، والموضة لأخرى
if deal.get("category") == "إلكترونيات":
    await client.send_message(TECH_CHANNEL, formatted, ...)
elif deal.get("category") == "موضة وأزياء":
    await client.send_message(FASHION_CHANNEL, formatted, ...)
```

---

## 💰 التكلفة التقريبية

| الخدمة | التكلفة |
|--------|---------|
| Railway | مجاناً (500 ساعة/شهر) |
| Claude Haiku | ~$0.001 لكل 100 عرض |
| تيليجرام | مجاناً |
| **الإجمالي** | **شبه مجاني** |

---

## 🛠️ حل المشاكل

**البوت لا يستلم رسائل:**
- تأكد أنه مضاف كـ Admin في القنوات المصدر
- تحقق من `SOURCE_CHANNELS` في .env

**خطأ في Claude:**
- تحقق من `ANTHROPIC_API_KEY`
- تأكد من وجود رصيد في الحساب

**فشل الإرسال للقناة:**
- تأكد أن البوت مضاف كـ Admin في DEST_CHANNEL
