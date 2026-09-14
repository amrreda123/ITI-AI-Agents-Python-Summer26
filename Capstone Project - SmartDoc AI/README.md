# 🚀 Capstone Project - SmartDoc AI

<div align="center">

**معهد تكنولوجيا المعلومات (ITI) — مسار تطوير وكلاء الذكاء الاصطناعي باستخدام بايثون**  
*المدرب:* م. فاطمة الراعي  
*الطالب:* عمرو رضا  

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-red?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-GenAI-orange?style=for-the-badge&logo=google)

</div>

---

## 📑 نظرة عامة

**SmartDoc AI** عبارة عن واجهة برمجة تطبيقات (API) مخصصة لإدارة المستندات واسترجاعها بذكاء باستخدام الذكاء الاصطناعي وهي جاهزة للإنتاج. يجمع المشروع بين جميع مهارات المسار:
- **تصميم FastAPI REST API:** بنية متعددة الطبقات (Layered architecture)، تنظيم باستخدام APIRouter، التحقق من صحة البيانات باستخدام مخططات Pydantic v2، رموز حالة استجابة متوقعة، وتوثيق تفاعلي تلقائي Swagger/OpenAPI.
- **تخزين البيانات وتهجير قواعد البيانات (Migrations):** استخدام SQLAlchemy 2.0 ORM مع SQLite، إدارة دورة الحياة بشكل مباشر باستخدام `with Session(engine) as db:`، وتطور مخطط قاعدة البيانات بالتحكم في الإصدارات باستخدام **Alembic** (لإضافة عمود `ai_summary`).
- **تحليل مهيكل باستخدام GenAI:** دمج **واجهة برمجة تطبيقات Gemini API** باستخدام نموذج التوجيه **R-T-C-F** (الدور، المهمة، السياق، التنسيق) مع ضمان توافق البيانات مع مخطط JSON.
- **وكيل ذكاء اصطناعي مستقل للقراءة فقط (AI Agent):** وكيل آمن قادر على استدعاء أدوات قراءة فقط مسموح بها مسبقاً (`list_documents`, `get_document`, `search_documents`)، مع التحقق من معطيات الأدوات عبر Pydantic ووجود قيود تنفيذ مثل `MAX_STEPS = 5`.

---

## 🏗️ هيكلية المشروع

```text
Capstone Project - SmartDoc AI/
├── main.py                                  # نقطة إدخال تطبيق FastAPI ومجمع الموجهات
├── database.py                              # محرك SQLAlchemy والأساس التعريفي
├── models.py                                # نموذج المستند ORM (المعرف، العنوان، المحتوى، الأولوية، الوصف، ai_summary)
├── schemas.py                               # التحقق من صحة Pydantic ومخططات الاستجابة
├── settings.py                              # التكوين المركزي ومحمل البيئة
├── documents.db                             # ملف قاعدة بيانات SQLite
├── .env.example                             # نموذج البيئة
├── .env                                     # أسرار البيئة المحلية (متجاهل بواسطة git)
├── .gitignore                               # قواعد التجاهل في Git
├── requirements.txt                         # تبعيات المشروع المثبتة
├── documents_api.postman_collection.json    # مجموعة اختبار Postman الكاملة
├── test_suite.py                            # نص التحقق الآلي من العقود
├── README.md                                # وثائق المشروع وسجل التدقيق
├── routes/
│   ├── __init__.py
│   ├── documents.py                         # مسارات CRUD للمستندات وتحميل النصوص
│   └── ai.py                                # مسارات الوكيل والتحليل المهيكل للذكاء الاصطناعي
├── services/
│   ├── __init__.py
│   ├── gemini_service.py                    # عميل واجهة برمجة تطبيقات Gemini وتحليل R-T-C-F
│   └── agent_service.py                     # وكيل آمن لاستدعاء الأدوات مع قائمة بيضاء وقيود للتكرار
├── alembic.ini                              # تكوين تهجير Alembic
└── alembic/
    ├── env.py                               # بيئة تهجير Alembic (وضع الدفعات لـ SQLite)
    ├── script.py.mako                       # قالب المراجعة
    └── versions/
        ├── 001_initial_documents_schema.py  # إنشاء الجدول الأولي
        └── 002_add_ai_summary.py            # إضافة عمود ai_summary عبر Alembic
```

---

## ⚡ البدء السريع: الإعداد والتنفيذ

### 1. الاستنساخ وتثبيت التبعيات
```bash
cd "Capstone Project - SmartDoc AI"
pip install -r requirements.txt
```

### 2. تكوين متغيرات البيئة
انسخ ملف `.env.example` إلى `.env` وقم بملء مفتاح واجهة برمجة تطبيقات Gemini الخاص بك:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=sqlite:///documents.db
```

### 3. تشغيل تهجيرات قاعدة البيانات
قم بتطبيق كافة مراجعات المخطط حتى الإصدار الأخير (`head`):
```bash
python -m alembic upgrade head
```
للتحقق من حالة التهجير الحالية:
```bash
python -m alembic current
```

### 4. تشغيل التطبيق
```bash
python -m uvicorn main:app --reload --port 8000
```
- واجهة Swagger التفاعلية: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- واجهة ReDoc التفاعلية: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📊 اختبارات وتوثيق HTTP

| الطريقة | نقطة النهاية (Endpoint) | جسم الطلب / المعلمات | الحالة المتوقعة | الحالة الفعلية | الوصف |
|---|---|---|---|---|---|
| `GET` | `/health` | لا يوجد | `200 OK` | `200 OK` | فحص صحة تشغيل الخدمة |
| `GET` | `/documents` | لا يوجد | `200 OK` | `200 OK` | سرد كافة المستندات المحفوظة |
| `POST` | `/documents` | JSON مستند صالح | `201 Created` | `201 Created` | إنشاء مستند جديد من JSON |
| `POST` | `/documents` | JSON مستند غير صالح | `422 Unprocessable` | `422 Unprocessable` | فشل التحقق في Pydantic |
| `GET` | `/documents/{id}` | معرف رقمي موجود | `200 OK` | `200 OK` | استرجاع مستند واحد عبر المعرف |
| `GET` | `/documents/999999` | معرف غير موجود | `404 Not Found` | `404 Not Found` | معالجة الموارد المفقودة |
| `PUT` | `/documents/{id}` | تحديث ببيانات JSON | `200 OK` | `200 OK` | تحديث جزئي أو كلي للمستند |
| `DELETE` | `/documents/{id}` | معرف رقمي موجود | `200 OK` | `200 OK` | حذف المستند نهائياً |
| `POST` | `/documents/upload` | ملف `text/plain` صالح | `201 Created` | `201 Created` | رفع ملف نصي وحفظ محتواه |
| `POST` | `/documents/upload` | نوع ملف غير صالح | `400 Bad Request` | `400 Bad Request` | فرض صارم لنوع MIME |
| `POST` | `/documents/{id}/analyze` | معرف موجود | `200 OK` | `200 OK` | تحليل Gemini وتحديث قاعدة البيانات |
| `POST` | `/documents/999999/analyze` | معرف غير موجود | `404 Not Found` | `404 Not Found` | حماية التحليل للمستندات المفقودة |
| `POST` | `/agent/ask` | `{"message": "..."}` | `200 OK` | `200 OK` | استدلال أدوات وكيل الذكاء الاصطناعي |

---

## 🤖 المرحلة د — مراجعة التطوير بمساعدة الذكاء الاصطناعي

كما هو مطلوب في **المرحلة د (Stage D)** من مواصفات المشروع (Capstone)، تم استخدام مساعد برمجة يعمل بالذكاء الاصطناعي لتنفيذ ميزات محددة:

### 1. الموجه (Prompt) المستخدم:
```text
In routes/ai.py, implement POST /documents/{document_id}/analyze.
Reuse the existing Document ORM model and Session(engine) pattern.
Return 404 when the document is missing.
Do not change the existing CRUD routes.
Call gemini_service to generate structured JSON using R-T-C-F and persist the summary into Document.ai_summary.
Ensure all exceptions are safely handled without leaking internal tracebacks or secrets.
```

### 2. التحقق اليدوي والتصحيحات:
أثناء المراجعة اليدوية للكود المُنشأ:
1. **وضع الدفعات (Batch Mode) في SQLite لـ Alembic:** تم التحقق من تفعيل `render_as_batch=True` في `alembic/env.py` لتعديل الجداول وإضافة `ai_summary` في SQLite بأمان دون أخطاء إعادة إنشاء الجدول.
2. **التعامل الآمن مع الاستثناءات:** تم تصحيح استجابات الأخطاء `500` العامة لضمان عدم تسريب بيانات الاعتماد الحساسة (`GEMINI_API_KEY`) أو سلاسل اتصال قاعدة البيانات الداخلية في أجسام استجابة HTTP.
3. **القائمة البيضاء الصارمة والتحقق من المخطط:** تم التأكد من أن الوكيل في `services/agent_service.py` يتحقق بدقة من مدخلات الأدوات عبر Pydantic (`gt=0` للمعرفات) ويفرض قيد `MAX_STEPS = 5` لمنع حلقات الاستدلال اللانهائية للنموذج.

---

## 🛠️ الاختبار باستخدام Postman و cURL

### أمثلة موجه أوامر Windows (Command Prompt) / cURL:

**1. إنشاء مستند:**
```cmd
curl -i -X POST http://127.0.0.1:8000/documents ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"SmartDoc Notes\",\"content\":\"FastAPI combined with Gemini AI enables autonomous retrieval.\",\"priority\":3}"
```

**2. تحليل مستند:**
```cmd
curl -i -X POST http://127.0.0.1:8000/documents/1/analyze
```

**3. سؤال وكيل الذكاء الاصطناعي:**
```cmd
curl -i -X POST http://127.0.0.1:8000/agent/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"What documents are available and what are their priority levels?\"}"
```

### Postman:
قم باستيراد ملف [`documents_api.postman_collection.json`](./documents_api.postman_collection.json) مباشرة إلى Postman. تأتي المجموعة مُهيأة مسبقاً بعنوان `base_url` (`http://127.0.0.1:8000`) وطلبات اختبار شاملة لكافة مسارات النظام وسيناريوهات الفشل.

---

## 🔒 الأمان وأفضل الممارسات
- **لا توجد مفاتيح مضمنة في الكود (Hardcoded):** يتم تحميل الأسرار ديناميكيًا من متغيرات البيئة.
- **نظافة مساحة عمل Git:** تم استثناء `.env` و `*.db` بشكل صارم في `.gitignore`.
- **وكيل قراءة فقط:** وكيل الذكاء الاصطناعي مقيد تماماً بعمليات القراءة فقط (`SELECT`) ولا يمكنه تعديل أو حذف المستندات.
