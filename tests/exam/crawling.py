from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

URL = "http://localhost:5000"
FILE_PATH = "tests/data/posts.json"
DIR_PATH = os.path.dirname(FILE_PATH)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

with webdriver.Chrome(options=chrome_options) as driver:
    driver.get(URL)
    print("✅ index 페이지 접속 완료")

    post_lists = driver.find_element(By.XPATH, "//div[@data-testid='container-posts-list']")
    link_elements = post_lists.find_elements(By.TAG_NAME, "a")
    print("✅ post list 가져오기 성공")

    post_urls = []
    for link_element in link_elements:
        href = link_element.get_attribute("href")
        post_urls.append(href)

    posts = []
    for i, url in enumerate(post_urls):
        print(f"✅ {i}번 게시물 확인")
        driver.get(url)
        post_data = {}
        title = driver.find_element(By.TAG_NAME, "h1").text
        author = driver.find_element(By.XPATH, "//span[@data-testid='text-post-author']").text
        date = driver.find_element(By.XPATH, "//span[@data-testid='text-post-date']").text
        contents = []

        article = driver.find_element(By.TAG_NAME, "article")
        content_elements = article.find_elements(By.TAG_NAME, "p")

        for content_element in content_elements:
            contents.append(content_element.text)

        posts.append({
            'title': title,
            'author': author,
            'date': date,
            'contents': contents
        })
        print("=========추출된 데이터=========")
        print(f"title: {title}")
        print(f"author: {author}")
        print(f"date: {date}")
        print(f"contents: {contents}")
        print(f"=========✅ 데이터 추출 완료=========")


    if DIR_PATH and not os.path.exists(DIR_PATH):
        try:
            os.makedirs(DIR_PATH, exist_ok=True)
            print(f"✅ 디렉토리 생성 성공: {DIR_PATH}")
        except Exception as e:
            print(f"❌ 디렉토리 생성 실패: {e}")
            driver.quit()
        
    with open("tests/data/posts.json", "w", encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
        print(f"✅ JSON 파일 저장 성공: {FILE_PATH}")