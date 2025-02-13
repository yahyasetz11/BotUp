import time
import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Gunakan WebDriver Manager untuk otomatis download ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://sakurazaka46.com/s/s46/diary/detail/58786?ima=0000&cd=blog")
print(driver.title)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
images = driver.find_elements(By.TAG_NAME, "img")

# Temukan semua gambar
images = driver.find_elements(By.TAG_NAME, 'img')

# Buat folder untuk gambar
os.makedirs('images', exist_ok=True)

# Download gambar yang memiliki prefix "mob"
for i, img in enumerate(images):
    img_url = img.get_attribute('src')
    
    if img_url and "mob" in img_url.split("/")[-1]:  # Cek apakah nama file mengandung "mob"
        img_data = requests.get(img_url).content
        with open(f'images/image_{i}.jpg', 'wb') as f:
            f.write(img_data)
            print(f'Gambar {i} berhasil diunduh dari {img_url}')

driver.quit()
print("Semua gambar berhasil diunduh!")