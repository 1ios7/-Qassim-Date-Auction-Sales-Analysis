import os
import matplotlib.pyplot as plt
import cv2

data_path = 'dataset/cell_images'
categories = ['Parasitized', 'Uninfected']

print("--- جاري فحص مجلدات المشروع ---")

for category in categories:
    path = os.path.join(data_path, category)
    # الحصول على قائمة بأسماء الملفات (تجاهل الملفات المخفية إن وجدت)
    images = [img for img in os.listdir(path) if not img.startswith('.')]
    print(f"الفئة: {category} | عدد الصور المتوفرة: {len(images)}")

    # عرض أول صورة من كل فئة للتأكد
    sample_img_path = os.path.join(path, images[0])
    img_array = cv2.imread(sample_img_path)
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # تحويل الألوان للعرض الصحيح

    plt.figure()
    plt.imshow(img_rgb)
    plt.title(f"Sample from: {category}")
    plt.axis('off')

plt.show()