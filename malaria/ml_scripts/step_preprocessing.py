import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split

# إعدادات المعالجة
IMG_SIZE = 128  # توحيد المقاس إلى 128x128
data_path = 'dataset/cell_images'
categories = ['Parasitized', 'Uninfected']

data = []
labels = []

print("--- جاري معالجة الصور، قد يستغرق ذلك بضع دقائق ---")

for i, category in enumerate(categories):
    path = os.path.join(data_path, category)
    for img in os.listdir(path):
        try:
            # 1. قراءة الصورة
            img_array = cv2.imread(os.path.join(path, img))
            # 2. تغيير الحجم
            new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            # 3. الإضافة للقائمة
            data.append(new_array)
            labels.append(i) # 0 لـ Parasitized و 1 لـ Uninfected
        except Exception as e:
            pass

# تحويل القوائم إلى مصفوفات NumPy لسرعة المعالجة
data = np.array(data)
labels = np.array(labels)

# 4. التطبيع (Normalization) تحويل القيم لتصبح بين 0 و 1
data = data.astype('float32') / 255.0

# 5. تقسيم البيانات: 80% للتدريب و 20% للاختبار
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

print(f"تمت المعالجة بنجاح!")
print(f"عدد صور التدريب: {len(X_train)}")
print(f"عدد صور الاختبار: {len(X_test)}")

# حفظ البيانات المعالجة لاستخدامها في الخطوة القادمة دون الحاجة لإعادة المعالجة
np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)
print("تم حفظ البيانات المعالجة في ملفات .npy بنجاح!")