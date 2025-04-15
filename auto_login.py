# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00877F34C3E800121F87956EA23129EC79A550308BA1BFF72DAD0E16750D0B1125F0BB901EB3187B82EE4D34859CDFBAA375BED58A60D0D56E7424FBD009DB1C04F34101EAA6BAD88D3FB71601DEE89692798570C8D9D391548674FFDE408E1F0624DDAB0CBB692DFF8E3C8006FD5583A36A3781C1F653F90E3E1CF1BF5C675BC715172C16C473A15F99C22C512AD5B581B225A7BFD8051E3AEDA18726E87716A2E8F99D1C52030D95426693391947F8F9A616E7652A64FEA7FAFA4CE899DE5A8E11A6F7A7DE03F89E829A8638EE9A765F22EC0442ECE9FE529343D8585D3332543B26BCE2A934E635D399DC18533B0A3672783EC5B924812774A2BF5197FE9E0C085884FF00C80F4176BEC969A33F1FFA1CDDF7B5F0CE3C19D0601914C36B0F3E5C156A4F49F5086BEB5B546041B364EBA0AD267544425AA1631D4DDA372D7AB241ACB0DB35278194E92ADC0A893A243CF7024FB1787132EB0211B16952DFF47F"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
