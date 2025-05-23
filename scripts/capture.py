import io
import time
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import pyautogui
from utils.utils import set_logger


# Change this as needed
url = "https://www.canva.com/design/DAGn2OlvkkA/y7NhT-F9563-yWtrh6wUkQ/view?utm_content=DAGn2OlvkkA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h45b5897532#84"
more_button_class_name = "PuABGQ A_H5UA _3GeXMg BMOCzQ fOwrSw _6Mu4Ow FQ64gg uMo6Kw YnfReg vFBXLA"
first_page = 1
final_page = 84

# set logger
logger = set_logger("Canva to PDF Scraper")

logger.debug(f"url: {url}")
logger.debug(f"more_button_class_name: {more_button_class_name}")

logger.info("Start Processing")

try:
    logger.info("Starting Chrome Browser")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    # Wait for page to be fully loaded (from AJAX)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ":rd:")))

    # Hover over slide and wait for 5 seconds
    element = driver.find_element(By.XPATH, '//div[@class="i8uyCw _7vS1Yw _682gpw"]')
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(5)

    logger.info("Capturing each slide")
    for page in range(final_page, first_page-1, -1):
        # Capture a specific region of the screen
        region_screenshot = pyautogui.screenshot(region=(360, 135, 1200, 900)) # x, y, width, height
        region_screenshot.save(f"./picture_output/{page}.png")
        ActionChains(driver).key_down(Keys.ARROW_LEFT).perform()
        time.sleep(0.5)
    
    logger.info("Capturing Success")

except Exception as err:
    raise err

finally:
    driver.quit()

logger.info("Using captured image to export to pdf")

images_list = []

for page in range(first_page, final_page+1):
    picture_path = f"./picture_output/{page}.png"
    print(f"processing page: {page}")

    with open(picture_path, "rb") as f:
        image_byte = f.read()

    image_bytes_stream = io.BytesIO(image_byte)
    image = Image.open(image_bytes_stream)
    image_loaded = image.copy()  # Fully loads the image into memory
    image_bytes_stream.close()

    images_list.append(image_loaded)

print("Done saving images")

print("Saving to PDF")
# Convert to RGB and save to PDF
images_rgb = [img.convert("RGB") for img in images_list]
images_rgb[0].save(
    "./output/output_capture.pdf",
    "PDF",
    resolution=100.0,
    save_all=True,
    append_images=images_rgb[1:]
)
print("Done saving to PDF")