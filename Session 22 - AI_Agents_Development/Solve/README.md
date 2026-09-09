# Lab 3 Solution: Build an n8n Agent Workflow with Gemini and Business Tools
**Course:** AI Agents Development & Agentic Automation (Day 3)  
**Instructor:** Eng. Fatma Elraey  

---

## 📑 جدول المحتويات
1. [✓ Quick Check — الأسئلة السريعة وإجاباتها](#-quick-check--before-you-start)
2. [الهدف العام من اللاب](#-الهدف-العام-من-اللاب)
3. [المخطط الهيكلي للـ Workflow](#-مخطط-الـ-workflow-في-n8n)
4. [خطوات تطبيق اللاب في n8n](#-خطوات-تطبيق-اللاب)
5. [ملفات الحل المرفقة](#-ملفات-الحل-المرفقة)

---

## ✓ Quick Check — Before You Start

### **Q1. What is the main benefit of n8n for this day?**
> **الإجابة:** الأتمتة البصرية المعتمدة على الأحداث (Visual event-driven orchestration) للربط فائق السرعة بين نماذج الذكاء الاصطناعي وتطبيقات الأعمال (SaaS / Webhooks / APIs).

---

### **Q2. Should an AI Agent node receive unrestricted tools?**
> **الإجابة:** لا. يجب منح الـ Agent فقط الصلاحيات والأدوات المحددة التي يحتاجها المسار (مبدأ Least Privilege)، وتكون أدوات القراءة منفصلة عن أدوات الإرسال والكتابة الحساسة.

---

## 🎯 الهدف العام من اللاب

بناء مسار وكيل ذكي مرئي داخل **n8n** يستقبل طلبات الدعم الفني عبر **Webhook**، ويتصل بنموذج **Gemini** مع ذاكرة محادثة (**Memory Buffer**)، ويستعلم عن بيانات الأوردر من **Google Sheets** كأداة قراءة فقط، مع وجود بوابة مراجعة قبل إرسال الرسائل عبر Slack أو Gmail.

---

## 🏗️ مخطط الـ Workflow في n8n

```
[ Webhook Trigger ] (POST /agent-support)
        │
        ▼
[ AI Agent Node ] ◄── [ Google Gemini Chat Model ]
        ▲        ◄── [ Window Buffer Memory (Session Key: ticket_id) ]
        │        ◄── [ Google Sheets / Mock Tool (Read-Only) ]
        ▼
[ Respond to Webhook ] (JSON Response with ticket_id, status, message)
```

---

## 🛠️ خطوات تطبيق اللاب

1. **إنشاء نقطة استقبال الـ Webhook:**
   - نوع الطلب: `POST`
   - المسار: `/webhook-test/agent-support`
   - الـ Payload المتوقع:
     ```json
     {
       "ticket_id": "T-204",
       "customer_id": "C-104",
       "message": "My shipment is late. Please update me."
     }
     ```

2. **إضافة عقدة الـ AI Agent وموديل Gemini:**
   - ضبط التعليمات الإرشادية (System Message):
     > *"You are a customer-support operations agent. Use connected tools for live customer or order data. Never invent balances, order status, or contact details."*

3. **إضافة الذاكرة (Short-Term Memory):**
   - ربط عقدة **Window Buffer Memory**.
   - ضبط مفتاح الجلسة (Session Key) على: `{{ $json.body.ticket_id }}` لضمان عزل ذاكرة كل تذكرة عن الأخرى.

4. **ربط أداة القراءة (Google Sheets / API Tool):**
   - قراءة بيانات العميل برقم `customer_id` أو `order_id` بدون صلاحيات كتابة أو حذف.

5. **توليد الرد النهائي المنظم (Respond to Webhook):**
   - إرجاع الرد بصيغة JSON:
     ```json
     {
       "ticket_id": "{{ $('Webhook Trigger').item.json.body.ticket_id }}",
       "status": "processed",
       "message": "{{ $json.output }}"
     }
     ```

---

## 📂 ملفات الحل المرفقة

| الملف | الوصف |
| :--- | :--- |
| [`n8n_agent_workflow.json`](./n8n_agent_workflow.json) | ملف الـ Workflow الكامل جاهز لعمل **Import** داخل n8n مباشرة بنقرة واحدة. |
| [`webhook_simulator.py`](./webhook_simulator.py) | كود بايثون لاختبار إرسال الـ Webhook وتجربة الـ Multi-turn memory. |
| [`mock_business_api.py`](./mock_business_api.py) | سيرفر FastAPI تجريبي يحاكي شيت جوجل ونقطة النهاية لاختبار الـ Agent محلياً. |
