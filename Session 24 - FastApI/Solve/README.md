# ITI - Python Framework with FastAPI
## Lab 2: Harden the API with Validation, Uploads & Errors

---

### 🚀 تشغيل التطبيق (How to Run)

1. **تثبيت الحزم المطلوبة (Dependencies):**
   ```bash
   pip install pydantic python-multipart python-dotenv uvicorn fastapi
   ```

2. **الدخول إلى مجلد `Solve`:**
   ```bash
   cd "Session 24 FastApI/Solve"
   ```

3. **تشغيل السيرفر باستخدام Uvicorn:**
   ```bash
   uvicorn main:app --reload
   ```

4. **فتح التوثيق التفاعلي للـ API:**
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 🧪 أوامر الاختبار والتجربة (cURL Commands)

#### 1. فحص الصحة وإعدادات البيئة (Health Check):
```bash
curl -X GET http://127.0.0.1:8000/health
```
**الرد المتوقع (HTTP 200 OK):**
```json
{
  "status": "ok",
  "app_name": "Documents API"
}
```

---

#### 2. جلب جميع المستندات (GET All Documents):
```bash
curl -X GET http://127.0.0.1:8000/documents
```

---

#### 3. جلب مستند محدد بواسطة الـ ID:
```bash
# مستند موجود
curl -X GET http://127.0.0.1:8000/documents/1

# مستند غير موجود (يرجع خطأ مهيكل Structured Error 404)
curl -X GET http://127.0.0.1:8000/documents/999
```
**رد الخطأ المهيكل (Structured Error 404):**
```json
{
  "error": {
    "code": "document_not_found",
    "message": "Document with ID 999 not found"
  }
}
```

---

#### 4. إنشاء مستند جديد بنجاح (POST - 201 Created):
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Docker Guide", "content": "Comprehensive Docker container guide", "priority": 3}'
```

---

#### 5. اختبار التحقق التلقائي للبيانات (Pydantic 422 Unprocessable Entity):
```bash
# عنوان قصير جداً (أقل من 3 حروف) وقيمة أولوية غير مسموحة (> 5)
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "A", "content": "", "priority": 10}'
```

---

#### 6. اختبار منع تكرار العنوان (Business Rule AppError 400):
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "FastAPI Notes", "content": "Duplicate title test", "priority": 1}'
```
**رد الخطأ المهيكل (Structured Error 400):**
```json
{
  "error": {
    "code": "duplicate_title",
    "message": "A document with this title already exists"
  }
}
```

---

#### 7. تعديل مستند (PUT):
```bash
curl -X PUT http://127.0.0.1:8000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "FastAPI Masterclass", "content": "Updated content with advanced validation", "priority": 5}'
```

---

#### 8. حذف مستند (DELETE):
```bash
curl -X DELETE http://127.0.0.1:8000/documents/1
```

---

#### 9. رفع ملف نصي أو PDF (POST /documents/upload):
```bash
# رفع ملف نصي مسموح به
curl -X POST http://127.0.0.1:8000/documents/upload \
  -F "file=@sample.txt"
```
**الرد المتوقع (HTTP 200 OK):**
```json
{
  "filename": "sample.txt",
  "content_type": "text/plain",
  "size": 128
}
```

---

### 📝 إجابات أسئلة الـ Checkpoints (من ملف اللاب):

- **Checkpoint — Exercise 1:**
  - **Q1:** Which field is server-owned?  
    **A:** `id`; it belongs in the response model (`DocumentResponse`) but not the create request model (`DocumentCreate`).

- **Checkpoint — Exercise 2:**
  - **Q1:** Does invalid input enter the endpoint body?  
    **A:** No. FastAPI and Pydantic reject it at the boundary first, returning an automatic `422 Unprocessable Entity` status.

- **Checkpoint — Exercise 3:**
  - **Q1:** Which content type does a file form use?  
    **A:** `multipart/form-data`.

- **Checkpoint — Exercise 4:**
  - **Q1:** What belongs in .env.example?  
    **A:** Variable names and safe default/placeholder values, not sensitive production secrets or keys.

- **Checkpoint — Exercise 5:**
  - **Q1:** Why is a structured error better than arbitrary strings?  
    **A:** Because client applications can reliably inspect and programmatically handle known error fields (like `error.code` and `error.message`) instead of parsing arbitrary text.
