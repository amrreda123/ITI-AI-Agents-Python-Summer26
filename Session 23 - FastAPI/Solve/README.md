# ITI - Python Framework with FastAPI
## Lab 1: Build a JSON-Only Documents REST API

---

### 🚀 تشغيل التطبيق (How to Run)

1. ادخل على مجلد `Solve`:
   ```bash
   cd "Session 23 FastAPI/Solve"
   ```

2. شغّل السيرفر باستخدام Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

3. افتح التوثيق التفاعلي (Swagger UI):
   - رابط Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - رابط ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 🧪 أوامر الاختبار السريعة (cURL Commands)

#### 1. فحص الصحة (Health Check):
```bash
curl -X GET http://127.0.0.1:8000/health
```

#### 2. جلب كل المستندات مع فلترة وبحث:
```bash
curl -X GET "http://127.0.0.1:8000/documents?q=fastapi&limit=10"
```

#### 3. جلب مستند محدد بالـ ID:
```bash
# مستند موجود (200 OK)
curl -X GET http://127.0.0.1:8000/documents/1

# مستند غير موجود (404 Not Found)
curl -X GET http://127.0.0.1:8000/documents/999
```

#### 4. إنشاء مستند جديد (POST):
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Docker Basics", "content": "Containerization intro"}'
```

#### 5. تعديل مستند (PUT):
```bash
curl -X PUT http://127.0.0.1:8000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "FastAPI Advanced Notes", "content": "Async, dependencies and Pydantic"}'
```

#### 6. حذف مستند (DELETE):
```bash
curl -X DELETE http://127.0.0.1:8000/documents/1
```

---

### 📝 إجابات أسئلة الـ Checkpoints (من ملف اللاب):

- **Before You Start:**
  - **Q1:** What command runs the development server?  
    **A:** `uvicorn main:app --reload`
  - **Q2:** What format should every application endpoint return?  
    **A:** JSON.

- **Exercise 1:**
  - **Q1:** What should GET /health return?  
    **A:** HTTP 200 with JSON `{"status": "ok"}`.

- **Exercise 2:**
  - **Q1:** What should /documents/999 return?  
    **A:** 404 Not Found (`{"detail": "Document not found"}`).

- **Exercise 3:**
  - **Q1:** Why use 201 instead of 200?  
    **A:** The request created a new resource (`HTTP_201_CREATED`).

- **Exercise 4:**
  - **Q1:** What method updates/replaces a resource in this lab?  
    **A:** PUT.

- **Exercise 5:**
  - **Q1:** What is the difference between `/documents/1` and `?limit=1`?  
    **A:** The first identifies one specific resource (Path Parameter); the second modifies a collection request (Query Parameter).
