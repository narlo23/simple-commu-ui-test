from exam_helpers import (get_driver, make_dir, save_json, navigate_to, get_post_urls, extract_post_data)

def save_posts_to_json(driver):
    post_urls = get_post_urls(driver)
    if not post_urls:
        print("🚨 추출할 게시물 URL이 없습니다. 프로그램을 종료합니다.")
        return
    
    posts = []
    for i, url in enumerate(post_urls):
        print(f"✅ {i+1}번 게시물 확인")
        post_data = extract_post_data(driver, url)
        
        if post_data:
            posts.append(post_data)

    print("\n=== 데이터 저장 시작 ===")
    make_dir(driver)
    save_json("posts", posts)


if __name__ == "__main__":
    driver = get_driver()
    navigate_to(driver, "/")
    print("✅ index 페이지 접속 완료")

    try:
        save_posts_to_json(driver)
    except AssertionError as ae:
        print(f"❗ Assertion 오류 발생: {ae}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("브라우저를 닫고 있습니다...")
        driver.quit()
        print("✅ 완료")