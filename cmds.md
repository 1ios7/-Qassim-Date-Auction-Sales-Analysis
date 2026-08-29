# يسوي بيئة افتراضية باسم .venv داخل مجلد المشروع (يعزل باكجات بايثون للمشروع هذا بس)
python -m venv .venv

# يفعّل البيئة الافتراضية عشان الأوامر/التثبيت يصير داخلها
.venv\Scripts\activate

# يحدّث pip (مدير تثبيت الباكجات) لتقليل مشاكل التثبيت
python -m pip install --upgrade pip

# يثبت إطار Django داخل البيئة الافتراضية
pip install django

# ينشئ مشروع Django باسم config داخل نفس المجلد الحالي (النقطة تعني “هنا”)
django-admin startproject config .

# ينشئ تطبيق جديد داخل المشروع باسم auctions
python manage.py startapp auctions

# يجهّز/ينشئ ملفات الترحيل (migrations) بناءً على تغييرات الـ models
python manage.py makemigrations

# يطبق الترحيلات على قاعدة البيانات ويجهز الجداول
python manage.py migrate

# ينشئ مستخدم أدمن (Superuser) للدخول على لوحة التحكم /admin
python manage.py createsuperuser

# يشغل السيرفر المحلي عشان تفتح الموقع بالمتصفح
python manage.py runserver


[http://127.0.0.1:8000](http://127.0.0.1:8000)