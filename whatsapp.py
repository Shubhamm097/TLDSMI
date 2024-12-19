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

# Step 2: Open WhatsApp Web and Log In
driver.get("https://web.whatsapp.com/")
print("Please scan the QR code to log in.")

# Wait for manual login
time.sleep(30)  # Adjust if needed

# Step 3: Navigate to the Desired Chat
chat_name = "Your Chat Name"  # Replace with the chat or group name
search_box = driver.find_element(By.XPATH, "//div[@title='Search input textbox']")
search_box.click()
time.sleep(1)
search_box.send_keys(chat_name)
time.sleep(2)
chat = driver.find_element(By.XPATH, f"//span[@title='{chat_name}']")
chat.click()
time.sleep(3)

# Step 4: Scroll to Load Messages and Media
for _ in range(5):  # Adjust the number of scrolls as needed
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - 500;", 
                          driver.find_element(By.XPATH, "//div[@class='_5kRIK']"))
    time.sleep(2)

# Step 5: Locate and Download Images
images = driver.find_elements(By.XPATH, "//img[contains(@src, 'blob:')]")  # Locate image blobs

# Create a folder to save images
os.makedirs("whatsapp_images", exist_ok=True)

for idx, img in enumerate(images):
    src = img.get_attribute("src")
    if src:
        # Open the image in WhatsApp Web
        img.click()
        time.sleep(2)

        # Find the actual image (expanded view)
        expanded_img = driver.find_element(By.XPATH, "//img[contains(@src, 'blob:')]")
        expanded_src = expanded_img.get_attribute("src")

        # Download the image
        response = requests.get(expanded_src)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            image = Image.open(img_data)
            image.save(f"whatsapp_images/image_{idx + 1}.png")
            print(f"Saved image_{idx + 1}.png")

        # Close the expanded view
        driver.find_element(By.XPATH, "//div[@aria-label='Close']").click()
        time.sleep(1)

# Close the browser
driver.quit()
