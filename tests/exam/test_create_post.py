from exam_helpers import get_driver, navigate_to, get_element_by_testid, click_element
from test_login import login_success
import constants

def create_post_success(driver):
    login_success()

    click_element(driver, "button-create-post")
    
    assert driver.current_url == "http://localhost:5000/post/create", "❌ 게시물 생성 페이지로 이동 실패"


if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    try:
        create_post_success()
    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")