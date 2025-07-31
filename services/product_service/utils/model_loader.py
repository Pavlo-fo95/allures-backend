import requests
from tensorflow.keras.models import load_model
from tempfile import NamedTemporaryFile

def load_remote_model():
    file_id = "1QSUv9D0i-3YhsaXBbEgBaRAStIsz19_n"  # замените на свой ID
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(url)
    response.raise_for_status()

    with NamedTemporaryFile(suffix=".h5") as tmp:
        tmp.write(response.content)
        tmp.flush()
        model = load_model(tmp.name)
        return model
