# ITI - Python Framework with FastAPI
## Lab 3: Simple ORM Persistence with SQLite & SQLAlchemy

---

### 🚀 تشغيل التطبيق (How to Run)

1. **تثبيت الحزم المطلوبة (Dependencies):**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

2. **الدخول إلى مجلد `Solve`:**
   ```bash
   cd "Session 25 - FastApI/Solve"
   ```

3. **تشغيل السيرفر باستخدام Uvicorn:**
   ```bash
   uvicorn main:app --reload
   ```

4. **فتح التوثيق التفاعلي للـ API:**
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 🧪 أوامر التجربة والاختبار (cURL Commands)

#### 1. فحص الصحة (Health Check):
```bash
curl -X GET http://127.0.0.1:8000/health
```

---

#### 2. إنشاء مستند جديد في قاعدة البيانات (POST - 201 Created):
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "SQLAlchemy Guide", "content": "Learn ORM persistence with SQLite", "priority": 3}'
```
**الرد المتوقع (مع ID تم توليده من الداتابيز):**
```json
{
  "id": 1,
  "title": "SQLAlchemy Guide",
  "content": "Learn ORM persistence with SQLite",
  "priority": 3
}
```

---

#### 3. جلب جميع المستندات المحفوظة (GET All Documents):
```bash
curl -X GET http://127.0.0.1:8000/documents
```

---

#### 4. جلب مستند محدد بالـ ID:
```bash
# مستند موجود
curl -X GET http://127.0.0.1:8000/documents/1

# مستند غير موجود (404 Not Found)
curl -X GET http://127.0.0.1:8000/documents/999
```

---

#### 5. تعديل مستند محفوظ (PUT):
```bash
curl -X PUT http://127.0.0.1:8000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Mastering SQLAlchemy", "content": "Advanced queries and sessions", "priority": 5}'
```

---

#### 6. حذف مستند (DELETE):
```bash
curl -X DELETE http://127.0.0.1:8000/documents/1
```

---

#### 7. البحث عن مستندات (GET /search):
```bash
curl -X GET "http://127.0.0.1:8000/search?q=SQLAlchemy&limit=10"
```

---

### 📝 إجابات أسئلة الـ Checkpoints (من ملف اللاب):

- **Checkpoint — Exercise 1:**
  - **Q1:** What does the engine point SQLAlchemy to?  
    **A:** The database location/URL we want to connect to (e.g., `sqlite:///documents.db`).

- **Checkpoint — Exercise 2:**
  - **Q1:** What does create_all(engine) do in this lab?  
    **A:** It checks the database metadata and creates any missing database tables defined by the ORM models (like the `documents` table).

- **Checkpoint — Exercise 3:**
  - **Q1:** Why use the `with Session(engine)` block?  
    **A:** It opens a new database session for the duration of the code block and guarantees that the session is automatically closed when the block exits.

- **Checkpoint — Exercise 4:**
  - **Q1:** Which call actually saves the new row?  
    **A:** `db.commit()`.

- **Checkpoint — Exercise 5:**
  - **Q1:** How do you prove persistence is real?  
    **A:** By creating a document using `POST /documents`, restarting the Uvicorn server, and then making a `GET /documents/{id}` request to confirm that the document is still present in `documents.db` and was not lost.
