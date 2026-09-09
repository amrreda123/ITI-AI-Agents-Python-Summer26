# Lab 2 Solution: Build a Stateful LangGraph Agent with Human Approval
**Course:** AI Agents Development & Agentic Automation (Day 2)  
**Instructor:** Eng. Fatma Elraey  

---

## 📑 جدول المحتويات
1. [✓ Quick Check — الأسئلة السريعة وإجاباتها](#-quick-check--before-you-start)
2. [الهدف العام من اللاب](#-الهدف-العام-من-اللاب)
3. [خطوات اللاب الستة بالتفصيل](#-خطوات-اللاب-الستة-بالتفصيل)
4. [ملفات الكود المنفذة](#-ملفات-الكود-المنفذة)
5. [المقارنة بين LangGraph و CrewAI](#-مقارنة-سريعة-langgraph-vs-crewai)

---

## ✓ Quick Check — Before You Start

### **Q1. What identifies one persisted conversation/run?**
> **الإجابة:** `thread_id` داخل الـ Configuration الخاصة بالـ Graph (`config={"configurable": {"thread_id": "..."}}`).

---

### **Q2. What lets a graph resume after an interrupt?**
> **الإجابة:** وجود **Checkpointer** (مثل `InMemorySaver`) مع تمرير نفس الـ `thread_id` عند عمل Resume عبر `Command(resume=...)`.

---

## 🎯 الهدف العام من اللاب

الانتقال من الـ Native Tool Loop العادية إلى بناء **Stateful AI Workflow باستخدام مكتبة LangGraph**، مع تطبيق:
1. حفظ حالة المحادثة وتتبعها عبر الـ Threads والـ Checkpointers.
2. إضافة ميزة **Human-in-the-Loop (HITL)** لإيقاف الـ Agent مؤقتاً عند العمليات الحساسة (مثل إرسال إيميل أو خصم رصيد) وانتظار موافقة أو تعديل بشري.
3. دعم مسارات الموافقة، الرفض، والتعديل (`Approve / Reject / Edit`).
4. مقارنة معمارية الـ Graphs بـ CrewAI المبنية على الأدوار والمهام.

---

## 🛠️ خطوات اللاب الستة بالتفصيل

### **01. LangChain Gemini Integration (`01_gemini_langchain.py`)**
- استخدام `ChatGoogleGenerativeAI` من حزمة `langchain-google-genai`.
- ربط الموديل واختبار الاتصال الأساسي.

---

### **02. Define State and Nodes (`02_state_nodes.py`)**
- إنشاء الـ State المشتركة بـ `TypedDict` باسم `SupportState` وتحتوي على:
  - `request`: نص طلب العميل.
  - `draft`: مسودة الرد التي يولدها الـ AI.
  - `status`: حالة التذكرة (`new`, `drafted`, `ready`, `sent`, `cancelled`).
- تعريف الـ Nodes البرمجية (`draft_node`, `finalize_node`).

---

### **03. Build and Persist the Graph (`03_persist_graph.py`)**
- توصيل العقد والمسارات: `START -> draft -> finalize -> END`.
- تفعيل ميزة حفظ الحالة عبر `InMemorySaver()`.
- تشغيل الـ Graph مع تحديد `thread_id` فريد لكل محادثة.

---

### **04. Add Human Approval Interrupt (`04_human_approval.py`)**
- استخدام دالة `interrupt(...)` لإيقاف مسار التنفيذ مؤقتاً قبل إرسال الرسالة للعميل.
- انتظار قرار المستخدم واستئناف المسار باستخدام `Command(resume=True)` أو `Command(resume=False)`.

---

### **05. Reject and Edit Paths (`05_reject_and_edit.py`)**
- اختبار سيناريوهات الـ Human-in-the-Loop:
  1. مسار الرفض (**Rejection Path**): تغيير الحالة إلى `cancelled` وعدم إرسال الإيميل.
  2. مسار التعديل والموافقة (**Edit & Approve Path**): تعديل نص المسودة قبل الإرسال وتحديث الـ State.

---

### **06. CrewAI Comparison (`06_crewai_comparison.py`)**
- بناء نفس المهمة باستخدام نمط CrewAI (Agent + Task + Process.sequential).

---

## ⚖️ مقارنة سريعة: LangGraph vs CrewAI

| المعيار | LangGraph | CrewAI |
| :--- | :--- | :--- |
| **النمط الأساسي** | State Machine & Directed Graph (Nodes & Edges) | Role-Based & Task-Based Team |
| **التحكم والـ Determinism** | دقيق جداً في الانتقال بين الحالات والشروط والـ Interrupts | عالي المستوى معتمداً على تفاعل الشخصيات والأدوار |
| **Human-in-the-Loop** | مدمج بدقة عبر `interrupt()` و `Command(resume=...)` | يعتمد على إعدادات الـ Tasks |
| **متى تختاره؟** | عند الحاجة لـ Workflow معقد، محكم، وقابل للتحكم الدقيق في الإنتاج | عند الرغبة في محاكاة فريق عمل متعدد التخصصات بسرعة |
