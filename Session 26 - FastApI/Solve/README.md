# ITI - Python Framework with FastAPI
## Lab 4: Migrate, Modularize & Document the SQLite API

---

### 🚀 تشغيل التطبيق والـ Migrations (How to Run)

1. **تثبيت الحزم المطلوبة (Dependencies):**
   ```bash
   pip install fastapi uvicorn sqlalchemy alembic pydantic
   ```

2. **الدخول إلى مجلد `Solve`:**
   ```bash
   cd "Session 26 - FastApI/Solve"
   ```

3. **تطبيق الـ Migrations على قاعدة البيانات باستخدام Alembic:**
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

### 🧪 أوامر التجربة والاختبار (cURL Commands)

#### 1. فحص الصحة (Health Check):
```bash
curl -X GET http://127.0.0.1:8000/health
```

---

#### 2. إنشاء مستند جديد مع الحقل الإضافي `description` (POST):
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Alembic Guide",
    "content": "Database migrations in FastAPI",
    "priority": 3,
    "description": "Step-by-step guide to database schema versioning"
  }'
```

---

#### 3. جلب جميع المستندات (GET All):
```bash
curl -X GET http://127.0.0.1:8000/documents
```

---

#### 4. جلب مستند محدد بالـ ID (GET One):
```bash
# مستند موجود
curl -X GET http://127.0.0.1:8000/documents/1

# مستند غير موجود (404 Not Found)
curl -X GET http://127.0.0.1:8000/documents/999
```

---

#### 5. تعديل مستند (PUT):
```bash
curl -X PUT http://127.0.0.1:8000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Alembic Guide",
    "content": "Comprehensive DB migrations",
    "priority": 5,
    "description": "Updated description with auto-generated migrations"
  }'
```

---

#### 6. حذف مستند (DELETE):
```bash
curl -X DELETE http://127.0.0.1:8000/documents/1
```

---

### 📝 إجابات أسئلة الـ Checkpoints (من ملف اللاب):

- **Checkpoint — Exercise 1:**
  - **Q1:** Why import models before autogenerate?  
    **A:** The `Document` mapping must be registered in `Base.metadata` so Alembic can compare the models with the current database schema.

- **Checkpoint — Exercise 2:**
  - **Q1:** Which command applies the migration to `documents.db`?  
    **A:** `alembic upgrade head`.

- **Checkpoint — Exercise 3:**
  - **Q1:** What database pattern should remain unchanged in this lab?  
    **A:** Using `with Session(engine) as db:` directly inside the endpoints that touch the database.

- **Checkpoint — Exercise 4:**
  - **Q1:** Where can you interactively test the generated API documentation?  
    **A:** Open `/docs` for the interactive Swagger UI; `/redoc` is the reference-style documentation view.
