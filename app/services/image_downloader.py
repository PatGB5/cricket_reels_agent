# app/services/image_downloader.py

import os
import requests
from PIL import Image
from io import BytesIO

def download_image(image_url: str, save_path: str) -> bool:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
        return True
    except Exception as e:
        print(f"[Error] Failed to download image from {image_url}: {e}")
        return False

def download_images_from_facts(facts, save_dir="media/images"):
    os.makedirs(save_dir, exist_ok=True)
    for i, item in enumerate(facts):
        url = item.get("image_link")
        if url:
            filename = f"fact_{i+1}.jpg"
            save_path = os.path.join(save_dir, filename)
            success = download_image(url, save_path)
            if success:
                item["image_path"] = save_path
            else:
                item["image_path"] = None
    return facts
