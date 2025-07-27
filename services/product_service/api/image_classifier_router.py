# services/product_service/api/image_classifier_router.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

router = APIRouter()
model = load_model("common/models/image_classifier.h5")

# Категории, как использовались при обучении
class_names = [
    'art', 'automotive', 'bags', 'books', 'diy', 'electronics', 'fashion',
    'food', 'home', 'medical', 'military', 'office', 'outdoor',
    'personal_care', 'pets', 'sports', 'toys'
]

# Обновлённые категории с украинскими названиями
CATEGORY_DETAILS = {
    'art': ('art', 'Товари для творчості', 'Drawing', 'Sketchbooks'),
    'automotive': ('automotive', 'Автотовари', 'Accessories', 'Car Mats'),
    'bags': ('bags', 'Сумки та рюкзаки', 'Accessories', 'Bags'),
    'books': ('books', 'Книги', 'Genres', 'Fiction'),
    'diy': ('diy', 'DIY та інструменти', 'Tools', 'Hammer'),
    'electronics': ('electronics', 'Ґаджети та новинки', 'Tech', 'Smartwatch'),
    'fashion': ('fashion', 'Одяг та взуття', 'Apparel', 'Clothing'),  # default footwear — отдельно не предсказывается
    'food': ('food', 'Їжа та напої', 'Grocery', 'Snacks'),
    'home': ('home', 'Домашній декор та меблі', 'Interior', 'Decor'),
    'medical': ('medical', 'Медичні товари', 'Care', 'Thermometer'),
    'military': ('military', 'Військові товари', 'Uniforms', 'Boots'),
    'office': ('office', 'Офісні товари', 'Stationery', 'Pens'),
    'outdoor': ('outdoor', 'Товари для відпочинку', 'Camping', 'Tents'),
    'personal_care': ('personal_care', 'Догляд за собою', 'Makeup', 'Lipstick'),
    'pets': ('pets', 'Товари для тварин', 'Care', 'Bowls'),
    'sports': ('sports', 'Спорттовари', 'Training', 'Dumbbells'),
    'toys': ('toys', 'Дитячі іграшки', 'Outdoor', 'Toys'),
    # Если добавишь поддержку этих категорий в модель — включи:
    'beauty': ('beauty', 'Краса та догляд', 'Skin Care', 'Cream'),
    'gadgets': ('gadgets', 'Ґаджети та новинки', 'Tech', 'Smartwatch'),
}

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

        category_code, category_name, subcategory, product_type = CATEGORY_DETAILS.get(
            predicted_class, (predicted_class, "Невідома категорія", None, None)
        )

        return {
            "predicted_category": predicted_class,
            "category_name": category_name,
            "subcategory": subcategory,
            "product_type": product_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
