# ITI - Python Framework with FastAPI
## Lab 5: Capstone — Test & Deliver the Lecture 4 API

---

### 🚀 تشغيل التطبيق وقاعدة البيانات (How to Run)

1. **تثبيت الحزم المطلوبة (Dependencies):**
   ```bash
   pip install -r requirements.txt
   ```

2. **الدخول إلى مجلد `Solve`:**
   ```bash
   cd "Session 27 - FastApI/Solve"
   ```

3. **تطبيق الـ Migrations على قاعدة البيانات:**
   ```bash
   alembic upgrade head
   ```

4. **تشغيل السيرفر باستخدام Uvicorn:**
   ```bash
   uvicorn main:app --reload
   ```

5. **استعراض التوثيق التفاعلي للـ API:**
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **OpenAPI JSON:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

### 🧪 أوامر الاختبار والتجربة عبر cURL (Smoke Test)

#### 1. فحص صحة التطبيق (Health Check):
```bash
curl -i http://127.0.0.1:8000/health
```

---

#### 2. إنشاء مستند جديد صالح (POST - 201 Created):
```bash
curl -i -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Capstone Document",
    "content": "Comprehensive testing and delivery of Documents API.",
    "priority": 3,
    "description": "Verified in Lab 5 Capstone"
  }'
```

---

#### 3. جلب جميع المستندات (GET All - 200 OK):
```bash
curl -i http://127.0.0.1:8000/documents
```

---

#### 4. جلب مستند محدد بواسطة الـ ID (GET One - 200 OK):
```bash
curl -i http://127.0.0.1:8000/documents/1
```

---

#### 5. تعديل مستند موجود (PUT - 200 OK):
```bash
curl -i -X PUT http://127.0.0.1:8000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Capstone Document (Updated)",
    "content": "Updated content after test verification.",
    "priority": 5,
    "description": "Updated description"
  }'
```

---

#### 6. حذف مستند (DELETE - 200 OK):
```bash
curl -i -X DELETE http://127.0.0.1:8000/documents/1
```

---

#### 7. محاولة جلب مستند محذوف/غير موجود (GET - 404 Not Found):
```bash
curl -i http://127.0.0.1:8000/documents/999999
```

---

#### 8. محاولة إنشاء مستند ببيانات غير صالحة (POST - 422 Validation Error):
```bash
curl -i -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "A", "content": "", "priority": 10}'
```

---

### 📬 اختبار الـ API باستخدام Postman

تم تضمين ملفات Postman الجاهزة داخل مجلد `Solve`:
- **Collection:** `documents_api.postman_collection.json`
- **Environment:** `documents_api.postman_environment.json`

**خطوات الاستيراد والتشغيل:**
1. افتح تطبيق Postman واضغط على **Import**.
2. اختر الملفين المذكورين أعلاه.
3. اختر الـ Environment المسمى **Documents API - Localhost**.
4. شغل الـ Requests بالترتيب للتحقق من جميع حالات الـ CRUD والأخطاء.

---

### 📊 جدول التحقق من العقود البرمجية (Contract Verification Matrix)

| Method | Endpoint | Test Case | Expected Status | Actual Status | Result |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `GET` | `/health` | Application health check | `200 OK` | `200 OK` | ✅ PASS |
| `GET` | `/documents` | List all persisted documents | `200 OK` | `200 OK` | ✅ PASS |
| `POST` | `/documents` | Valid payload with description | `201 Created` | `201 Created` | ✅ PASS |
| `POST` | `/documents` | Invalid payload (title < 3, priority > 5) | `422 Unprocessable` | `422 Unprocessable` | ✅ PASS |
| `GET` | `/documents/{id}` | Read existing document | `200 OK` | `200 OK` | ✅ PASS |
| `GET` | `/documents/{id}` | Read non-existing ID (`999999`) | `404 Not Found` | `404 Not Found` | ✅ PASS |
| `PUT` | `/documents/{id}` | Update existing document fields | `200 OK` | `200 OK` | ✅ PASS |
| `DELETE` | `/documents/{id}`| Delete existing document | `200 OK` | `200 OK` | ✅ PASS |

---

### 📝 إجابات أسئلة الـ Checkpoints (من ملف اللاب):

- **Checkpoint — Exercise 1:**
  - **Q1:** Why check the migration revision before final testing?  
    **A:** To ensure that the database schema in `documents.db` is up-to-date and matches the SQLAlchemy ORM models (including all new columns like `description`) before accepting client traffic.

- **Checkpoint — Exercise 2:**
  - **Q1:** What should every curl check record?  
    **A:** The HTTP status code line (e.g., `HTTP/1.1 200 OK`) and the JSON response body structure.

- **Checkpoint — Exercise 3:**
  - **Q1:** Why use `{{base_url}}`?  
    **A:** To make the Postman collection modular and easily switchable between environments (Localhost, Staging, Production) without modifying individual request URLs.

- **Checkpoint — Exercise 4:**
  - **Q1:** Is a 200 response enough to call a test passed?  
    **A:** No; the response payload structure, field types, and headers must also conform to the promised OpenAPI / Pydantic contract (such as `DocumentResponse`).

- **Checkpoint — Exercise 5:**
  - **Q1:** What architecture should the final lab use?  
    **A:** The modular architecture from Lecture 4: `database.py` (Engine/Base), `models.py` (SQLAlchemy ORM with `description`), `schemas.py` (Pydantic), `routes/documents.py` (`APIRouter` with `with Session(engine) as db`), `alembic/` migrations, and `main.py` app assembly.
