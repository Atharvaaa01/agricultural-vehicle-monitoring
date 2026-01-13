import os
import time
import random
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ================= CONFIG =================
SAVE_DIR = "dataset/images/train"

SEARCH_TERMS = [
    "tractor agriculture india",
    "truck carrying sugarcane india",
    "bullock cart agriculture india",
    "sugarcane loaded tractor",
    "indian vehicle number plate"
]
# =========================================

os.makedirs(SAVE_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def download_images(query):
    target_count = random.randint(10, 50)
    print(f"\n🔍 {query} → Target images: {target_count}")

    driver.get("https://www.google.com/imghp")
    time.sleep(3)

    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)

    image_urls = set()
    scrolls = 0

    while len(image_urls) < target_count and scrolls < 15:
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")

        for thumb in thumbnails:
            try:
                thumb.click()
                time.sleep(1)
                images = driver.find_elements(By.CSS_SELECTOR, "img.iPVvYb")

                for img in images:
                    src = img.get_attribute("src")
                    if src and src.startswith("http"):
                        image_urls.add(src)
            except:
                pass

        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        scrolls += 1

    count = 0
    for url in image_urls:
        if count >= target_count:
            break
        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            filename = f"{query.replace(' ', '_')}_{count}.jpg"
            img.save(os.path.join(SAVE_DIR, filename))
            count += 1
        except:
            pass

    print(f"✅ Downloaded {count} images for {query}")

for term in SEARCH_TERMS:
    download_images(term)

driver.quit()
print("\n🎉 ALL RANDOM IMAGES DOWNLOADED SUCCESSFULLY")
