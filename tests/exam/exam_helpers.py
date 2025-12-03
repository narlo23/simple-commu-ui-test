from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import constants
import json
import os

def save_screenshots(driver, name: str, dir=constants.SCREENSHOT_DIR):
    if not os.path.exists(dir):
        os.makedirs(dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(dir, filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

    return filepath

'''
make driver
'''
def get_driver():
    """Create and return a Chrome WebDriver instance."""
    chrome_options = Options()
    # Set HEADLESS=true for headless mode (default is false for local browser window)
    if os.environ.get("HEADLESS", "false").lower() != "false":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def make_dir(driver, path=constants.DIR_PATH):    
    if path and not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            print(f"✅ 디렉토리 생성 성공: {path}")
        except Exception as e:
            print(f"❌ 디렉토리 생성 실패: {e}")
            driver.quit()

def save_json(filename, data):
    with open(f"tests/data/{filename}.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ JSON 파일 저장 성공: {constants.FILE_PATH}")
    print(f"✅ 총 {len(data)}개의 데이터 저장 완료")

def navigate_to(driver, path: str):
    if path.lower().startswith(('http://', 'https://')):
        full_url = path
    else:
        full_url = f"{constants.BASE_URL}{path}"
    driver.get(full_url)
    print(f"✅ 접속 시도: {full_url}")

def wait_for_element(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be present."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )

def wait_for_url_contains(driver, url_part: str, timeout: int = 10):
    """Wait for URL to contain specified string."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.url_contains(url_part))

def get_element_by_testid(driver, test_id: str):
    """Get element by data-testid attribute."""
    return driver.find_element(By.CSS_SELECTOR, f'[data-testid="{test_id}"]')

def get_element_by_tagname(driver, tag_name: str):
    return driver.find_element(By.TAG_NAME, tag_name)

def get_post_urls(driver):
    try:
        post_lists = get_element_by_testid(driver, "container-posts-list")
        print("✅ post list 가져오기 성공")
    except Exception as e:
        print(f"❌ Post list 컨테이너를 찾을 수 없습니다: {e}")
        return []
    
    link_elements = post_lists.find_elements(By.TAG_NAME, "a")
    post_urls = [
        link_element.get_attribute("href")
        for link_element in link_elements
        if link_element.get_attribute("href")
    ]

    print(f"✅ 총 {len(post_urls)}개의 게시물 URL 추출 성공")
    return post_urls

def extract_post_data(driver, url: str):
    print(f"--- 게시물 URL: {url} 확인 시작 ---")
    navigate_to(driver, url)

    try:
        title = get_element_by_testid(driver, "text-post-title").text

        author = get_element_by_testid(driver, "text-post-author").text
        date = get_element_by_testid(driver, "text-post-date").text
        
        article = get_element_by_testid(driver, "text-post-content")
        content_elements = article.find_elements(By.TAG_NAME, "p")
        contents = [content_element.text for content_element in content_elements]

        post_data = {
            'title': title,
            'author': author,
            'date': date,
            'contents': contents
        }
        
        print(f"=========✅ 데이터 추출 완료: {title[:20]}... =========")
        return post_data
    except Exception as e:
        print(f"❌ 데이터 추출 중 오류 발생 ({url}): {e}")
        return None
    

def get_local_storage_value(driver, key = constants.LOCAL_STORAGE_KEY):
    local_storage_data = driver.execute_script(f"return window.localStorage.getItem('{key}');")

    if local_storage_data is not None:
        print(f"✅ 로컬 스토리지 '{key}' 값: {local_storage_data}")    
    else:
        print(f"❌ 로컬 스토리지에 '{key}' 키가 존재하지 않습니다.")

def wait_for_element_clickable(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be clickable."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )

def click_element(driver, test_id: str):
    """Click element with data-testid."""
    element = wait_for_element_clickable(driver, test_id)
    element.click()
    return element

def check_cookie(driver, key):
    login_cookie = driver.get_cookie(key)
    if login_cookie is not None:
        print("✅ 쿠키 정보 확인 완료")
        print(f"쿠키 값: {login_cookie.get('value')}")
    assert login_cookie is not None, f"❌ 쿠키 '{key}'가 존재하지 않습니다."

def search_posts(driver):
    posts = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/post/')]")
    assert len(posts) > 0, "❌ 검색 결과가 없습니다."
    print(f"✅ 총 {len(posts)}개의 게시물 확인")
    post_urls = [post.get_attribute("href") for post in posts]

    return post_urls

def extract_and_check_post_data(driver, post_urls, expected_keyword:str):
    for i, url in enumerate(post_urls):
        print(f"--- {i+1}번째 검색 결과 게시물 ({url}) 확인 시작 ---")

        navigate_to(driver, url)

        expected_keyword = expected_keyword.lower()
        try:
            title = get_element_by_testid(driver, "text-post-title").text.lower()
            author = get_element_by_testid(driver, "text-post-author").text.lower()
            contents_text = get_element_by_testid(driver, "text-post-content").text.lower()
        except Exception as e:
            print(f"❌ 데이터 추출 오류: {e}")
            continue

        is_keyword_in_post = expected_keyword in title or expected_keyword in author or expected_keyword in contents_text
        assert is_keyword_in_post, f"❌ {i+1}번째 게시물 제목/내용에 키워드 '{expected_keyword}'가 없습니다."
        print(f"✅ {i+1}번째 게시물에서 키워드 '{expected_keyword}' 검증 성공")

def count_posts(driver):
    post_list_container = get_element_by_testid(driver, "container-posts-list")
    link_elements = post_list_container.find_elements(By.TAG_NAME, "a")

    count = len(link_elements)
    print(f"✅ 'container-posts-list' 내부에 총 {count}개의 <a> 태그가 확인되었습니다.")
    return count