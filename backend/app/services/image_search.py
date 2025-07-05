import os
from serpapi import GoogleSearch
import httpx
from PIL import Image
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def fetch_image_url(query: str) -> str:
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set in environment.")

    search = GoogleSearch({
        "q": query,
        "tbm": "isch",  # image search
        "api_key": api_key,
        "ijn": "0",  # page index
        "num": "1"   # number of results
    })

    try:
        results = search.get_dict()
        images = results.get("images_results", [])
        if images:
            return images[0]["original"]  # direct image URL
    except Exception as e:
        print(f"[Error] Failed image search for '{query}': {e}")
    
    return None

async def download_image(image_url: str, save_path: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        img.save(save_path)
        print(f"[Success] Image saved to {save_path}")
        return True
    except Exception as e:
        print(f"[Error] Failed to download image from {image_url}: {e}")
        return False

async def download_images_from_facts(facts, save_dir="downloaded_images"):
    os.makedirs(save_dir, exist_ok=True)

    today_str = datetime.today().strftime('%Y%m%d')
    print(f"[Info] Downloading images to directory: {save_dir}")

    facts_with_image_path = []

    for i, item in enumerate(facts):
        query = item.get("image_query")
        fact_text = item.get("fact")
        print(f"[Info] Fetching image for query: {query}")

        image_path = None
        if query:
            url = await fetch_image_url(query)
            # url = None
            if url:
                filename = f"{query.replace(' ', '_')}_{today_str}.jpg"
                save_path = os.path.join(save_dir, filename)
                success = await download_image(url, save_path)
                if success:
                    image_path = save_path

        facts_with_image_path.append({
            "fact": fact_text,
            "image_path": image_path
        })

    return facts_with_image_path

# # Example usage
# if __name__ == "__main__":
#     async def main():
#         query = "Mahela Jayawardene cricket"
#         image_url = await fetch_image_url(query)
#         if image_url:
#             print(f"Image URL for '{query}': {image_url}")
#         else:
#             print(f"No image found for '{query}'.")
#         filename = "mahela_jayawardene.jpg"
#         save_dir = "downloaded_images"
#         save_path = os.path.join(save_dir, filename)
#         success = await download_image(image_url, save_path)
#         if success:
#             print(f"Image downloaded successfully to {save_path}")
#         else:
#             print("Image download failed.")

#     asyncio.run(main())