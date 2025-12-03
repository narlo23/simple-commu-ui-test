from exam_helpers import get_driver, navigate_to, click_element, get_element_by_testid, wait_for_url_contains, check_cookie, wait_for_element
import constants

USERNAME = constants.USERNAME
PASSWORD = constants.PASSWORD

def login_success(driver):
    click_element(driver, "link-login")
    print("✅ 로그인 버튼 클릭, 로그인 페이지로 이동중")

    username = get_element_by_testid(driver, "input-username")
    username.clear()
    username.send_keys(USERNAME)

    password = get_element_by_testid(driver, "input-password")
    password.clear()
    password.send_keys(PASSWORD)

    click_element(driver, "button-login-submit")
    print("✅ 버튼 클릭: 로그인 요청 전송 및 리다이렉션 시작")

    assert wait_for_url_contains(driver, "/"), "❌ 오류: 메인페이지로 이동하지 못했습니다."
    print("✅ URL 검증 성공: 메인 페이지로의 리다이렉션이 완료되었습니다.")

    login_username = get_element_by_testid(driver, "text-username").text
    welcome_username = get_element_by_testid(driver, "text-welcome-username").text
    print(f"유저명: {login_username}, 회원가입한 유저명: {USERNAME}")
    assert login_username == USERNAME and welcome_username == USERNAME, "❌ 오류: 유저명이 일치하지 않습니다.."
    print("✅ 유저명 검증 성공: 정상 로그인되었습니다.")

    check_cookie(driver, "connect.sid")

def invalid_username(driver):
    click_element(driver, "link-login")
    print("✅ 로그인 버튼 클릭, 로그인 페이지로 이동중")

    username = get_element_by_testid(driver, "input-username")
    username.clear()
    username.send_keys(constants.INVALID_USERNAME)

    password = get_element_by_testid(driver, "input-password")
    password.clear()
    password.send_keys(constants.INVALID_PASSWORD)

    click_element(driver, "button-login-submit")
    print("✅ 버튼 클릭: 로그인 요청 전송 및 리다이렉션 시작")

    alert_msg = wait_for_element(driver, "alert-login-error")
    assert alert_msg.is_displayed(), "❌ alert 메시지가 확인되지 않습니다."
    print(f"✅ 오류 메시지 확인: {alert_msg.text}")


def invalid_password(driver):
    click_element(driver, "link-login")
    print("✅ 로그인 버튼 클릭, 로그인 페이지로 이동중")

    username = get_element_by_testid(driver, "input-username")
    username.clear()
    username.send_keys(USERNAME)

    password = get_element_by_testid(driver, "input-password")
    password.clear()
    password.send_keys(constants.INVALID_PASSWORD)

    click_element(driver, "button-login-submit")
    print("✅ 버튼 클릭: 로그인 요청 전송 및 리다이렉션 시작")

    alert_msg = wait_for_element(driver, "alert-login-error")
    assert alert_msg.is_displayed(), "❌ alert 메시지가 확인되지 않습니다."
    print(f"✅ 오류 메시지 확인: {alert_msg.text}")

def logout(driver):
    click_element(driver, "button-user-menu")
    print("✅ 유저 버튼 클릭: 로그아웃 팝업 확인")

    logout_btn = wait_for_element(driver, "button-logout")
    assert logout_btn.is_displayed(), "❌ 로그아웃 버튼이 확인되지 않습니다."

    click_element(driver, "button-logout")
    print("✅ 로그아웃 버튼 클릭")

    login_btn = wait_for_element(driver, "link-login")
    assert login_btn.is_displayed(), "❌ 로그아웃이 정상적으로 이뤄지지 않았습니다."
    print("✅ 로그인 버튼 확인")

if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    try:
        print("1. 올바르지 않은 유저명")
        print("=" * 20)
        invalid_username(driver)
        print("=" * 20)

        print("2. 올바르지 않은 비밀번호")
        print("=" * 20)
        invalid_password(driver)
        print("=" * 20)

        print("3. 로그인 성공 케이스")
        print("=" * 20)
        login_success(driver)
        print("=" * 20)

        print("4. 로그아웃")
        print("=" * 20)
        logout(driver)
        print("=" * 20)

    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")