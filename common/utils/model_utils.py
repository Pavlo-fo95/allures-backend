import os

MODEL_PATH = "common/models/image_classifier.h5"

def check_model_exists():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"❌ Модель не найдена: {MODEL_PATH}")
    print("✅ Модель найдена:", MODEL_PATH)