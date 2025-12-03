from exam_helpers import get_driver, navigate_to, click_element, wait_for_url_contains, get_element_by_testid, search_posts, extract_and_check_post_data
import constants

KEYWORD = constants.KEYWORD

def search_process():
    click_element(driver, "link-nav-search")

    assert wait_for_url_contains(driver, "/search"), "❌ 오류: 검색 페이지로 이동하지 못했습니다."
    print("✅ URL 검증 성공: 검색 페이지로의 리다이렉션이 완료되었습니다.")

    search_field = get_element_by_testid(driver, "input-search")
    search_field.send_keys(KEYWORD)

    click_element(driver, "button-search")
    print("✅ 버튼 클릭: 검색 시작")

    post_urls = search_posts(driver)
    extract_and_check_post_data(driver, post_urls, KEYWORD)



if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")

    try:
        search_process()
    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")