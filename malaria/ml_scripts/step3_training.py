import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# 1. تحميل البيانات المعالجة التي حفظناها في الخطوة السابقة
print("--- جاري تحميل البيانات المعالجة ---")
X_train = np.load('X_train.npy')
y_train = np.load('y_train.npy')
X_test = np.load('X_test.npy')
y_test = np.load('y_test.npy')

# 2. بناء معمارية الشبكة العصبية (CNN)
model = models.Sequential([
    # الطبقة الأولى: استخراج الميزات (مثل الحواف والأشكال)
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),

    # الطبقة الثانية: استخراج أنماط أكثر تعقيداً
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # الطبقة الثالثة
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # تحويل البيانات من مصفوفة إلى خط مستقيم لتدخل في الطبقات الكثيفة
    layers.Flatten(),
    layers.Dense(64, activation='relu'),

    # طبقة المخرجات: نتيجتان فقط (مصاب أو سليم)
    layers.Dense(2, activation='softmax')
])

# 3. إعداد عملية التدريب (Compilation)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 4. بدء التدريب الفعلي
print("--- بدء عملية التدريب ---")
# سنقوم بالتدريب لـ 10 دورات (Epochs)، يمكنك زيادتها لاحقاً لزيادة الدقة
history = model.fit(X_train, y_train, epochs=10,
                    validation_data=(X_test, y_test),
                    batch_size=32)

# 5. حفظ النموذج المدرب (هذا هو "الملف العبقري" الذي سنستخدمه في موقع الويب)
model.save('malaria_model.h5')
print("--- تم تدريب النموذج وحفظه باسم malaria_model.h5 بنجاح! ---")