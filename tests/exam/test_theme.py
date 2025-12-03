from exam_helpers import get_driver, navigate_to, save_screenshots, get_local_storage_value, click_element, get_root_html_element

def change_theme(driver):
    try:
        print("✅ 접속 완료: 기본은 라이트모드")
        save_screenshots(driver, "default")

        click_element(driver, "button-theme-toggle")
        print("✅ 테마 변경 버튼 클릭: 다크모드로 변경")
        save_screenshots(driver, "dark_mode")

        html_element = get_root_html_element(driver)
        print(f"현재 모드: {html_element.get_attribute('class')}")

        get_local_storage_value(driver)

        click_element(driver, "button-theme-toggle")
        print("✅ 테마 변경 버튼 다시 클릭: 라이트모드로 변경")
        save_screenshots(driver, "light_mode")

        print(f"현재 모드: {html_element.get_attribute('class')}")

        get_local_storage_value(driver)

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

    change_theme(driver)