from exam_helpers import get_driver, wait_for_url_contains, navigate_to, click_element, get_element_by_testid, check_cookie

USERNAME = "abcd"
PASSWORD = "1234"

def signup_success():
    try:
        click_element(driver, "link-signup")
        print("✅ 회원가입 버튼 클릭, 회원가입 페이지로 이동중")

        username = get_element_by_testid(driver, "input-username")
        username.send_keys(USERNAME)

        password = get_element_by_testid(driver, "input-password")
        password.send_keys(PASSWORD)

        confirm_password = get_element_by_testid(driver, "input-confirm-password")
        confirm_password.send_keys(PASSWORD)

        click_element(driver, "button-signup-submit")
        print("✅ 버튼 클릭: 회원가입 요청 전송 및 리다이렉션 시작")
        
        assert wait_for_url_contains(driver, "/"), "❌ 오류: 메인페이지로 이동하지 못했습니다."
        print("✅ URL 검증 성공: 메인 페이지로의 리다이렉션이 완료되었습니다.")

        login_username = get_element_by_testid(driver, "text-username").text
        print(f"유저명: {login_username}, 회원가입한 유저명: {USERNAME}")
        assert login_username == USERNAME, "❌ 오류: 유저명이 일치하지 않습니다.."
        print("✅ 유저명 검증 성공: 정상 로그인되었습니다.")

        check_cookie(driver, "connect.sid")

    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")


if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    signup_success()

