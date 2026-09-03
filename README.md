 # 🌴 Qassim Date Auction & Sales Analysis

## 📌 نبذة عن المشروع

**مزاد القصيم للتمور وتحليل المبيعات** هو مشروع تخرج يهدف إلى تطوير منصة رقمية متكاملة لإدارة عمليات مزاد التمور، وتوفير خدمات إلكترونية للمستخدمين والبائعين وأصحاب المتاجر والموظفين.

يجمع المشروع بين **إدارة المزادات، المتاجر والمنتجات، المزايدات، تحليل المبيعات، لوحات المعلومات، والذكاء الاصطناعي** ضمن منصة واحدة.

---

## 🚀 مميزات المشروع

### 🏷️ نظام المزادات
- إنشاء وإدارة المزادات.
- عرض المزادات المتاحة.
- المزايدة على المنتجات.
- إدارة صور المزادات.
- متابعة عمليات المزايدة.
- مراجعة وإدارة المزادات.

### 🛒 المتاجر والمنتجات
- إنشاء ملفات للمتاجر.
- عرض المتاجر والمنتجات.
- إدارة المنتجات.
- إضافة المنتجات إلى سلة المشتريات.
- إدارة عمليات التسوق.

### 👤 إدارة المستخدمين
- تسجيل الدخول والخروج.
- إدارة حسابات المستخدمين.
- تحديد أدوار المستخدمين.
- لوحات تحكم مختلفة حسب نوع المستخدم.

### 📊 تحليل المبيعات
- تحليل بيانات المبيعات.
- عرض البيانات باستخدام الرسوم البيانية.
- تحليل أداء الفروع.
- عرض مؤشرات ونتائج المبيعات.
- إمكانية تحميل التقارير.

### 🤖 الذكاء الاصطناعي
- دمج نموذج ذكاء اصطناعي لتحليل صور الملاريا.
- رفع صورة للحصول على نتيجة التنبؤ.
- استخدام TensorFlow وKeras.
- استخدام OpenCV لمعالجة الصور.

### 👨‍💼 لوحة تحكم الموظفين
- متابعة النظام.
- إدارة المزادات.
- مراجعة العمليات.
- إدارة العمليات المختلفة داخل المنصة.

---

## 🛠️ التقنيات المستخدمة

| التقنية | الاستخدام |
|---|---|
| Python | لغة البرمجة الأساسية |
| Django | تطوير تطبيق الويب |
| SQLite | قاعدة البيانات |
| HTML | بناء صفحات الويب |
| CSS | تصميم الواجهات |
| JavaScript | التفاعل داخل الواجهات |
| Pandas | تحليل البيانات |
| NumPy | معالجة البيانات والعمليات الحسابية |
| Matplotlib | إنشاء الرسوم البيانية |
| Plotly | الرسوم البيانية التفاعلية |
| OpenCV | معالجة الصور |
| TensorFlow | الذكاء الاصطناعي |
| Keras | نموذج التعلم الآلي |
| Git | إدارة الإصدارات |
| GitHub | استضافة وإدارة المشروع |

---

## 📂 هيكل المشروع

```text
QassimDigitalAuction/
│
├── accounts/
├── auctions/
├── config/
├── malaria/
├── portal/
├── qassim_dashboard/
├── sales_analysis/
├── seller/
├── shops/
├── staffpanel/
├── media/
├── Screenshots/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🖼️ صور المشروع

## 🏠 واجهات النظام

### الصورة 01
![Project Screenshot 01](Screenshots/image1.png)

### الصورة 02
![Project Screenshot 02](Screenshots/image2.png)

### الصورة 03
![Project Screenshot 03](Screenshots/image3.png)

### الصورة 04
![Project Screenshot 04](Screenshots/image4.png)

### الصورة 05
![Project Screenshot 05](Screenshots/image5.png)

### الصورة 06
![Project Screenshot 06](Screenshots/image6.png)

### الصورة 07
![Project Screenshot 07](Screenshots/image7.png)

### الصورة 08
![Project Screenshot 08](Screenshots/image8.png)

### الصورة 09
![Project Screenshot 09](Screenshots/image9.png)

### الصورة 10
![Project Screenshot 10](Screenshots/image10.png)

### الصورة 11
![Project Screenshot 11](Screenshots/image11.png)

### الصورة 12
![Project Screenshot 12](Screenshots/image12.png)

### الصورة 13
![Project Screenshot 13](Screenshots/image13.png)

### الصورة 14
![Project Screenshot 14](Screenshots/image14.png)

### الصورة 15
![Project Screenshot 15](Screenshots/image15.png)

### الصورة 16
![Project Screenshot 16](Screenshots/image16.png)

### الصورة 17
![Project Screenshot 17](Screenshots/image17.png)

### الصورة 18
![Project Screenshot 18](Screenshots/image18.png)

---

# ⚙️ طريقة تشغيل المشروع

## 1. تحميل المشروع

```bash
git clone https://github.com/1ios7/-Qassim-Date-Auction-Sales-Analysis.git
```

## 2. الدخول إلى مجلد المشروع

```bash
cd -Qassim-Date-Auction-Sales-Analysis
```

## 3. إنشاء البيئة الافتراضية

```bash
python -m venv venv
```

## 4. تفعيل البيئة الافتراضية في Windows

```bash
venv\Scripts\activate
```

## 5. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

## 6. تشغيل المشروع

```bash
python manage.py runserver
```

ثم افتح:

```text
http://127.0.0.1:8000/
```

---

# 📊 مكونات النظام

| التطبيق | الوظيفة |
|---|---|
| `accounts` | إدارة الحسابات والمستخدمين |
| `auctions` | إدارة المزادات والمزايدات |
| `shops` | المتاجر والمنتجات والسلة |
| `seller` | وظائف البائع |
| `staffpanel` | لوحة الموظفين والإدارة |
| `portal` | بوابة النظام |
| `sales_analysis` | تحليل بيانات المبيعات |
| `qassim_dashboard` | لوحات المعلومات والتحليلات |
| `malaria` | تحليل الصور باستخدام الذكاء الاصطناعي |

---

# 🎓 مشروع التخرج

### اسم المشروع

**مزاد القصيم للتمور وتحليل المبيعات**

### فكرة المشروع

تطوير منصة رقمية متكاملة تجمع بين:

- إدارة المزادات.
- المزايدة الإلكترونية.
- إدارة المتاجر والمنتجات.
- سلة المشتريات.
- إدارة المستخدمين.
- لوحات التحكم.
- تحليل بيانات المبيعات.
- تحليل أداء الفروع.
- الذكاء الاصطناعي.

---

# 👨‍💻 المطور

**Zaidan Al-Mutairi**

**Diploma — Information Technology / Systems Design & Analysis**

---

## 📄 License

This project was developed as an academic graduation project.
