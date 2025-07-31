from fastapi import APIRouter, File, UploadFile, HTTPException
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from sqlalchemy.orm import Session
import numpy as np
import os
import requests

from common.db.session import SessionLocal
from common.models.categories import Category

router = APIRouter()

MODEL_PATH = "common/models/image_classifier.h5"
GOOGLE_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1HTRaFv4KTloWiGwE2ZKqJf4PHHgZeIr6"
# https://drive.google.com/file/d/1HTRaFv4KTloWiGwE2ZKqJf4PHHgZeIr6/view?usp=sharing   для h5
# https://drive.google.com/file/d/1cr3h1gGEuriaeXp15j1VmDhaRBa0yAgV/view?usp=sharing   для tflite

# Загрузка модели с Google Drive, если не существует локально
def download_model_if_needed():
    if not os.path.exists(MODEL_PATH):
        print("📦 Модель не найдена, загружаем с Google Drive...")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        try:
            response = requests.get(GOOGLE_DRIVE_URL)
            if response.status_code == 200:
                with open(MODEL_PATH, "wb") as f:
                    f.write(response.content)
                print("✅ Модель успешно скачана")
            else:
                raise HTTPException(status_code=500, detail="Ошибка загрузки модели с Google Drive")
        except Exception as e:
            print(f"❌ Ошибка при загрузке модели: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при скачивании модели")

# Предварительная загрузка модели в память
download_model_if_needed()
model = load_model(MODEL_PATH)

# Категории
class_names = [
    'art', 'automotive', 'bags', 'books', 'diy', 'electronics', 'fashion',
    'food', 'home', 'medical', 'military', 'office', 'outdoor',
    'personal_care', 'pets', 'sports', 'toys'
]

@router.post("/predict-category/")
async def predict_category(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        temp_path = f"temp_images/{file.filename}"
        os.makedirs("temp_images", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(contents)

        img = image.load_img(temp_path, target_size=(180, 180))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]

        db: Session = SessionLocal()
        category_obj = db.query(Category).filter(Category.category_name == predicted_class).first()

        if category_obj:
            result = {
                "predicted_category": predicted_class,
                "category_name": category_obj.description,
                "subcategory": category_obj.subcategory,
                "product_type": category_obj.product_type
            }
        else:
            result = {
                "predicted_category": predicted_class,
                "category_name": "Категорія не знайдена в БД",
                "subcategory": None,
                "product_type": None
            }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
