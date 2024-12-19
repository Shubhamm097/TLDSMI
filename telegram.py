import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import requests
from io import BytesIO

# Step 1: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 2: Open Telegram Web and Log In
driver.get("https://web.telegram.org/")
print("Please scan the QR code to log in.")

# Wait for manual login
time.sleep(30)

# Step 3: Navigate to the desired chat/channel
# Replace with the name of the chat/channel you want to access
chat_name = "Your Chat Name"
search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
search_box.send_keys(chat_name)
time.sleep(2)
chat = driver.find_element(By.XPATH, f"//span[text()='{chat_name}']")
chat.click()
time.sleep(3)

# Step 4: Scroll and Load Images
# Adjust the scrolling to load all images
for _ in range(5):  # Scroll 5 times (adjust as necessary)
    driver.execute_script("window.scrollBy(0, -500);")
    time.sleep(2)

# Step 5: Locate and Download Images
images = driver.find_elements(By.TAG_NAME, "img")

# Create a folder to save images
os.makedirs("telegram_images", exist_ok=True)

for idx, img in enumerate(images):
    src = img.get_attribute("src")
    if src and "blob:" not in src:  # Skip non-image blobs
        response = requests.get(src)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            image = Image.open(img_data)
            image.save(f"telegram_images/image_{idx + 1}.png")
            print(f"Saved image_{idx + 1}.png")

# Close the browser
driver.quit()
