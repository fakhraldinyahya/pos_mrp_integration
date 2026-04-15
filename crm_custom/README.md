# CRM Customization - Odoo 19 Community

Professional CRM module for Odoo 19 to enhance Sales Performance Analytics through lost, won, and churn reason tracking.

---

## 🌍 نظرة عامة (Overview)

هذا الموديل مخصص لتحسين أداء المبيعات في نظام أودو 19 من خلال تتبع وتحليل أسباب "الفوز" و"الخسارة" و"عدم التجديد" بدقة عالية، مما يساعد أصحاب القرار على اتخاذ خطوات تصحيحية بناءً على بيانات حقيقية.

This professional Odoo 19 module enhances CRM analytical capabilities by tracking multi-reason data for won, lost, and non-renewal (churn) scenarios, enabling data-driven sales strategies.

---

## ✨ المميزات الرئيسية (Key Features)

### 1. تتبع أسباب الفوز (Won Reasons Tracking) 🏆
- إجبار الموظف على اختيار سبب الفوز عند إغلاق الفرصة بنجاح.
- **Mandatory** reasons upon winning a deal to understand success drivers.

### 2. تعدد أسباب الخسارة (Multiple Lost Reasons) ❌
- إمكانية اختيار أكثر من سبب للخسارة بدلاً من سبب واحد فقط.
- Support for **multiple selection** of loss reasons for deeper analysis.

### 3. تحليل عدم التجديد (Churn/Non-Renewal Analysis) 🔄
- حقول خاصة لتتبع أسباب عدم تجديد العقود للعملاء الحاليين.
- Specialized tracking for **renewal-type** opportunities to monitor customer churn.

### 4. توافقية كاملة (Full Compatibility) ⚙️
- الحفاظ على توافق التقارير القديمة مع دعم الميزات الجديدة.
- **Backward compatible** with standard Odoo reports and pivot views.

### 5. تحسين واجهة المستخدم (UI/UX Optimizations) 🎨
- رفع حقل "اسم الفرصة" في الواجهة السريعة.
- إضافة تبويب "تحليل النجاح والفقد" في نموذج الفرصة.
- Clean and optimized interface for faster data entry.

---

## 🛠️ التثبيت (Installation)

1. وانقل مجلد `crm_custom` إلى مجلد الـ `addons` الخاص بك.
2. قم بتحديث قائمة الموديولات في أودو.
3. ابحث عن `CRM Customization` وقم بتثبيته.

1. Copy the `crm_custom` folder to your Odoo `addons` directory.
2. Update the Apps list in Odoo.
3. Search for `CRM Customization` and click Install.

---

## 📁 هيكلية الموديل (Module Structure)

```text
crm_custom/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── crm_lead.py      # الوراثة والمنطق البرمجي (Clean Code)
│   └── crm_reason.py    # نماذج الأسباب الجديدة
├── wizard/
│   ├── __init__.py
│   ├── crm_lead_lost.py # معالج الخسارة المطور
│   ├── crm_lead_lost_views.xml
│   ├── crm_lead_won.py  # معالج الفوز الجديد
│   └── crm_lead_won_views.xml
├── views/
│   └── crm_lead_views.xml # تخصيصات واجهات العرض
├── data/
│   └── crm_reason_data.xml # أسباب افتراضية جاهزة
└── security/
    └── ir.model.access.csv # صلاحيات الوصول
```

---

## 💎 الكود النظيف (Clean Code Standards)

تم بناء هذا الموديل باتباع معايير **Clean Code** و **PEP8**:
- **Separation of Concerns**: فصل المنطق البرمجي عن "المعالجات" (Wizards).
- **Readability**: تسميات واضحة وموثقة (Docstrings).
- **Performance**: عمليات قواعد بيانات محسنة.

---

### 📝 المطور (Developer)
**Antigravity AI (Pair Programming with Developer)**
*Built for business excellence and precision.*
