"""
Utility functions for Selenium UI automation tests.
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def get_driver():
    """Create and return a Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def save_screenshot(driver, name: str):
    """Save a screenshot with timestamp."""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath


def wait_for_element(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be present."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_element_clickable(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be clickable."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_element_visible(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be visible."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_url_contains(driver, url_part: str, timeout: int = 10):
    """Wait for URL to contain specified string."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.url_contains(url_part))


def get_element_by_testid(driver, test_id: str):
    """Get element by data-testid attribute."""
    return driver.find_element(By.CSS_SELECTOR, f'[data-testid="{test_id}"]')


def click_element(driver, test_id: str):
    """Click element with data-testid."""
    element = wait_for_element_clickable(driver, test_id)
    element.click()
    return element


def type_text(driver, test_id: str, text: str):
    """Type text into element with data-testid."""
    element = wait_for_element(driver, test_id)
    element.clear()
    element.send_keys(text)
    return element


def get_body_class(driver):
    """Get the class attribute of the body element."""
    body = driver.find_element(By.TAG_NAME, "body")
    return body.get_attribute("class") or ""


def generate_unique_username():
    """Generate a unique username for testing."""
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}"


def navigate_to(driver, path: str):
    """Navigate to a specific path."""
    driver.get(f"{BASE_URL}{path}")


def clear_session(driver):
    """Clear all cookies and local storage."""
    driver.delete_all_cookies()
    try:
        driver.execute_script("localStorage.clear();")
        driver.execute_script("sessionStorage.clear();")
    except:
        pass
