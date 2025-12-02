from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "http://localhost:5000/"

chrome_options = Options()
chrome_options.add_argument("--headless") # 백그라운드 실행 옵션
chrome_options.add_argument("--disable-dev-shm-usage")

USERNAME = "abcd"
PASSWORD = "1234"

def signup_success():
    with webdriver.Chrome(options=chrome_options) as driver:
        try:
            driver.get(url=URL)

            sign_up_button = driver.find_element(By.XPATH, "//a[@href='/signup']")
            sign_up_button.click()
            print("✅ 회원가입 버튼 클릭, 회원가입 페이지로 이동중")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "shadcn-card")))
            print("✅ 회원가입 페이지 로딩 완료")

            username = driver.find_element(By.ID, "username")
            username.send_keys(USERNAME)

            password = driver.find_element(By.ID, "password")
            password.send_keys(PASSWORD)

            confirm_password = driver.find_element(By.ID, "confirmPassword")
            confirm_password.send_keys(PASSWORD)

            create_button = driver.find_element(By.XPATH, "//button[@data-testid='button-signup-submit']")
            create_button.click()
            print("✅ 버튼 클릭: 회원가입 요청 전송 및 리다이렉션 시작")
            
            WebDriverWait(driver, 10).until(EC.url_to_be(URL))
            assert driver.current_url == URL, "❌ 오류: 메인페이지로 이동하지 못했습니다."
            print("✅ URL 검증 성공: 메인 페이지로의 리다이렉션이 완료되었습니다.")

            login_username = driver.find_element(By.XPATH, "//span[@data-testid='text-username']").text
            print(f"유저명: {login_username}, 회원가입한 유저명: {USERNAME}")
            assert login_username == USERNAME, "❌ 오류: 유저명이 일치하지 않습니다.."
            print("✅ 유저명 검증 성공: 정상 로그인되었습니다.")

            login_cookie = driver.get_cookie("connect.sid")
            if login_cookie is not None:
                print("✅ 쿠키 정보 확인 완료")
                print(f"쿠키 값: {login_cookie.get('value')}")
            assert login_cookie is not None, f"❌ 쿠키 'connect.sid'가 존재하지 않습니다."

        except AssertionError as ae:
            print(f"❗ Assertion 오류 발생: {ae}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        finally:
            print("브라우저를 닫고 있습니다...")
            driver.quit()
            print("✅ 완료")


if __name__ == "__main__":
    signup_success()

