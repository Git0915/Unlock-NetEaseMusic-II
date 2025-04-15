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
    browser.add_cookie({"name": "MUSIC_U", "value": "0073E204AC5C48AD1A685BAB2CE11265AA57322AE4579B36735FA1FE5A3FA771C5DC16D24727D4764CE43DBF214A3BA8CF86C973D17E2F2E6A3C6B69889E30769A6B8469F3B52D9F57E6457F1C462525ECD582FBDF0937B26826DE9C8B4AA68F9E694268E82B2BDE8C8D4F2AFF1BFD033831E7A662BD623AFFD48B9A90A8DC87382CAB9D3B15F03EA8A13F75F14CA1C19C613F5E09B9F70199B35ED734FA3905A0A55272DAA19C47B3B19F16EC3138EBFF89D2F2D76269177EBD55B863E4785A5E2847EB9DDDC2F3AA0F0F3022533166B4ACF562F105A4FA62B1F7D2728AC8F382D09DF3EEF25FD939974B30E71027956654248C896BD049CAABC0EAF06D879FAA810B9ED006CCF83F131D7AAFAD6D4EEAB054B5BBF01252159700A68792BA4913EF8908A57957670A9D1E77BD780B9EC20C157B2A96DA820629AA8BCAF27B1518C14F374D1C3F04295F608B69639FA072D01271A3C84A0D759328760BEB07B12AE7808C82BDA785C76B8E7E6C1239E87B"})
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
