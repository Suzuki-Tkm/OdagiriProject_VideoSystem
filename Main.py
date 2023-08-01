import os
from PIL import Image

def get_latest_image(folder):
    image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not image_files:
        return None
    latest_image = sorted(image_files, key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)[0]
    return os.path.join(folder, latest_image)

def display_latest_image(folder):
    latest_image_path = get_latest_image(folder)
    if latest_image_path is None:
        print("フォルダー内に画像が存在しません。")
        return
    image = Image.open(latest_image_path)
    image.show()
folder_path = "./picture"
display_latest_image(folder_path)
