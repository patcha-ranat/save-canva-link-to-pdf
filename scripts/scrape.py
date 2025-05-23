import io 
import time
import requests
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import list_union, set_logger


# Change this as needed
url = "https://www.canva.com/design/DAGn2OlvkkA/y7NhT-F9563-yWtrh6wUkQ/view?utm_content=DAGn2OlvkkA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h45b5897532"
more_button_class_name = "PuABGQ A_H5UA _3GeXMg BMOCzQ fOwrSw _6Mu4Ow FQ64gg uMo6Kw YnfReg vFBXLA"
each_grid_class_name = "tK5tJQ YVm1_w Sy5OHg"

# set logger
logger = set_logger("Canva to PDF Scraper")

logger.debug(f"url: {url}")
logger.debug(f"more_button_class_name: {more_button_class_name}")
logger.debug(f"each_grid_class_name: {each_grid_class_name}")

logger.info("Start Processing")

link_output = []

try:
    logger.info("Starting Chrome Browser")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    # Find & Click 'more' button to open grid
    driver.find_element(By.ID, ":rd:").click()
    
    # Find & Click 'Open in Grid View' button
    driver.find_element(By.XPATH, f"//button[@class='{more_button_class_name}']").click()
    
    # Wait for image link to be loaded (from AJAX) for each grid
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@class="vV0w_Q"]')))
    
    logger.info("Slowly scrolling down to the end of the page while saving image link")
    
    scrollable_element = driver.find_element(By.XPATH, f'//div[@class="li_efQ rKFvEA"]')
    total_height = int(driver.execute_script("return arguments[0].scrollHeight", scrollable_element))
    
    logger.info(f'scrollable height: {total_height}')
    
    logger.info("Save thumbnail image regarding links discovered order")
    for i in range(1, total_height, 500):
        driver.execute_script("arguments[0].scrollTop = arguments[1]", scrollable_element, i)
        time.sleep(0.125)
        element = driver.find_elements(By.XPATH, '//img[@class="vV0w_Q"]')
        
        link_output = list_union(link_output, [each.get_attribute("src") for each in element])
    
    logger.info(f"Saved links: {len(link_output)}")
    logger.info(f"Saved unique links: {len(set(link_output))}")
    logger.info("Success")

except Exception as err:
    raise err

finally:
    driver.quit()

logger.info("Using link to export thumbnail image to pdf")

try:
    images_list = []

    for idx, link in enumerate(link_output):
        logger.info(f"processing page: {idx+1}")
        response = requests.get(link).content

        image_bytes_stream = io.BytesIO(response)
        image = Image.open(image_bytes_stream)
        image_loaded = image.copy()  # Fully loads the image into memory
        image_bytes_stream.close()

        images_list.append(image_loaded)

    logger.info("Done saving images object from bytes")

    logger.info("Saving to PDF")
    # Convert to RGB and save to PDF
    images_rgb = [img.convert("RGB") for img in images_list]
    images_rgb[0].save(
        "./output/output_scrape.pdf",
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=images_rgb[1:]
    )
    logger.info("Done saving to PDF")

except Exception as err:
    raise err