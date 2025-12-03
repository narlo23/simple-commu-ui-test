from exam_helpers import get_driver, navigate_to, get_element_by_testid, click_element, get_element_by_tagname, count_posts
from test_login import login_success
import constants

def create_post_success(driver):
    login_success(driver)

    before_posts_count = count_posts(driver)

    click_element(driver, "button-create-post")
    
    assert driver.current_url == "http://localhost:5000/post/create", "❌ 게시물 생성 페이지로 이동 실패"
    print(f"✅ 게시물 생성 페이지로 이동 완료, 현재 URL: {driver.current_url}")

    post_title = get_element_by_testid(driver, "input-post-title")
    post_title.send_keys(constants.POST_TITLE)

    post_content = get_element_by_testid(driver, "textarea-post-content")
    post_content.send_keys(constants.POST_CONTENT)

    post_category = get_element_by_testid(driver, "input-post-category")
    post_category.send_keys(constants.POST_CATEGORY)

    print("=" * 30)
    '''
        content는 textarea라서 .text로 접근 가능하지만
        title, category는 input text라서 get_attribute("value")로 접근 가능
    '''
    print(f"title: {post_title.get_attribute('value')}")
    print(f"content: {post_content.text}")
    print(f"category: {post_category.get_attribute('value')}")
    print("=" * 30)

    click_element(driver, "button-create-post")
    print("✅ 게시물 생성 버튼 클릭")

    success_toast_message = get_element_by_tagname(driver, "ol")
    assert success_toast_message is not None, "❌ 토스트 메시지 확인 불가, 게시물 생성이 정상 처리되지 않았습니다."
    print("✅ 토스트 메시지 확인 완료, 게시물 생성이 정상 처리되었습니다.")

    click_element(driver, "button-back-home")
    print("✅ 홈으로 이동 완료")

    after_posts_count = count_posts(driver)
    print(before_posts_count, after_posts_count)
    assert before_posts_count + 1 == after_posts_count, "❌ 게시물이 정상적으로 생성되지 않았습니다."
    print(f"✅ 기존 개시물 개수: {before_posts_count}, 게시물 생성 후 개수: {after_posts_count}")

if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    try:
        create_post_success(driver)
    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")