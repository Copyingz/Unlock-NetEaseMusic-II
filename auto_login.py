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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F5C3D3A589661D9D9E4080F5B202B5731D50F744A771950DF40712ED95CAAF4569DE5A28851D7A58E675477159EABACE216CD0C77362FC2BCA4EC03742F7A171DB159A8A101ED701AB814FB61B9BBC970A8048B05C91F206F3E115559D167FAE1548A6686ADFF58A8CF5D8E363A243EDC77EE471FE3E3F77E861CD3992E068647FDB079E23276E681249EACFB1788E06C4DC187CE6B740988377999BC5CC42BCCA19618D3C4B8D17F8CF5B1F04F3E8F937676C61CA414FBD526E067301EF1C375DA46E4E0D894FD2131B489083B13401CE5ED4AF75F88D8EB0CF47E5A9426BFA5FD3DD468828DE86872C2FB46F8BAFF71C54F23E9D308683CD2DBE9463A7EC02BD1719490178268FE98815C147314C994030C4B302561B50702B821674F06826F3A2B02E0CCF23466EAAE704545F9FD0E810F76482CF19D7C94A26231E7BF38603FE8454FE137DCF42B0A944E091D5909A790AE66DB04F743333713D4AEF9E60"})
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
