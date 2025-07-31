import argparse
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import tensorflow as tf

DATA_DIR = 'datasets'
IMG_SIZE = (180, 180)
BATCH_SIZE = 16
EPOCHS = 5

# 1. Парсим аргумент
parser = argparse.ArgumentParser(description="Train or fine-tune the image classifier.")
parser.add_argument('--fine-tune', action='store_true', help="Use this flag to fine-tune the existing model.")
args = parser.parse_args()

# 2. Подготовка данных
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

num_classes = len(train_generator.class_indices)

# 3. Создание или загрузка модели
if args.fine_tune and os.path.exists("image_classifier.h5"):
    print("🔄 Загрузка существующей модели для дообучения...")
    model = load_model("image_classifier.h5")
else:
    print("🧠 Создание новой модели...")
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# 4. Обучение или дообучение
model.fit(train_generator, validation_data=val_generator, epochs=EPOCHS)

# 5. Сохранение модели
model.save("image_classifier.h5")
print("✅ Модель успешно сохранена как image_classifier.h5")
