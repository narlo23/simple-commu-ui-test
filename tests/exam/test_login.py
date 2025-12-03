from exam_helpers import get_driver, navigate_to, click_element, get_element_by_testid, wait_for_url_contains, check_cookie
import constants

USERNAME = constants.USERNAME
PASSWORD = constants.PASSWORD

def login_success(driver):
    click_element(driver, "link-login")
    print("✅ 로그인 버튼 클릭, 로그인 페이지로 이동중")

    username = get_element_by_testid(driver, "input-username")
    username.send_keys(USERNAME)

    password = get_element_by_testid(driver, "input-password")
    password.send_keys(PASSWORD)

    click_element(driver, "button-login-submit")
    print("✅ 버튼 클릭: 로그인 요청 전송 및 리다이렉션 시작")

    assert wait_for_url_contains(driver, "/"), "❌ 오류: 메인페이지로 이동하지 못했습니다."
    print("✅ URL 검증 성공: 메인 페이지로의 리다이렉션이 완료되었습니다.")

    login_username = get_element_by_testid(driver, "text-username").text
    print(f"유저명: {login_username}, 회원가입한 유저명: {USERNAME}")
    assert login_username == USERNAME, "❌ 오류: 유저명이 일치하지 않습니다.."
    print("✅ 유저명 검증 성공: 정상 로그인되었습니다.")

    check_cookie(driver, "connect.sid")

if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    try:
        login_success()
    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")