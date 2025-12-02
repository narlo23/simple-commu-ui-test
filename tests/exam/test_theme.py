from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os

URL = "http://localhost:5000/"
SCREENSHOT_DIR = os.path.dirname("tests/data/screenshots")
LOCAL_STORAGE_KEY = "theme"

chrome_options = Options()
chrome_options.add_argument("--headless") # 백그라운드 실행 옵션
chrome_options.add_argument("--disable-dev-shm-usage")

def save_screenshots(driver, name: str):
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

    return filepath

def get_local_storage_value(driver):
    local_storage_data = driver.execute_script(f"return window.localStorage.getItem('{LOCAL_STORAGE_KEY}');")

    if local_storage_data is not None:
        print(f"✅ 로컬 스토리지 '{LOCAL_STORAGE_KEY}' 값: {local_storage_data}")    
    else:
        print(f"❌ 로컬 스토리지에 '{LOCAL_STORAGE_KEY}' 키가 존재하지 않습니다.")

with webdriver.Chrome(options=chrome_options) as driver:
    try:
        driver.get(URL)
        print("✅ 접속 완료: 기본은 라이트모드")
        save_screenshots(driver, "default")

        theme_button = driver.find_element(By.XPATH, "//button[@data-testid='button-theme-toggle']")
        theme_button.click()
        print("✅ 테마 변경 버튼 클릭: 다크모드로 변경")
        save_screenshots(driver, "dark_mode")

        html_element = driver.find_element(By.TAG_NAME, "html")
        print(f"현재 모드: {html_element.get_attribute('class')}")

        get_local_storage_value(driver)

        theme_button.click()
        print("✅ 테마 변경 버튼 다시 클릭: 라이트모드로 변경")
        save_screenshots(driver, "light_mode")

        print(f"현재 모드: {html_element.get_attribute('class')}")

        get_local_storage_value(driver)

    except AssertionError as ae:
            print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")