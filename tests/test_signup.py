"""
Selenium tests for user signup functionality.
"""
import time
from utils import (
    get_driver,
    save_screenshot,
    wait_for_element,
    wait_for_url_contains,
    click_element,
    type_text,
    get_element_by_testid,
    generate_unique_username,
    navigate_to,
    clear_session,
    BASE_URL,
    log_test_step,
    logger
)


def test_signup_success():
    """Test successful user registration."""
    driver = get_driver()
    
    try:
        # log_test_step("Navigating to signup page")
        navigate_to(driver, "/signup")
        # save_screenshot(driver, "signup_page")
        
        # log_test_step("Generating unique username and password")
        username = generate_unique_username()
        password = "testpass123"
        
        # log_test_step(f"Entering username: {username}")
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        type_text(driver, "input-confirm-password", password)
        
        # save_screenshot(driver, "signup_form_filled")
        
        # log_test_step("Clicking signup submit button")
        click_element(driver, "button-signup-submit")
        
        # log_test_step("Waiting for redirect to home page")
        wait_for_url_contains(driver, "/")
        time.sleep(1)
        
        # log_test_step("Verifying username appears in navbar")
        username_element = wait_for_element(driver, "text-username")
        assert username in username_element.text, f"Expected username '{username}' in navbar"
        
        # save_screenshot(driver, "signup_success")
        # logger.info(f"SUCCESS: User '{username}' registered successfully")
        
    finally:
        driver.quit()


def test_signup_duplicate_id():
    """Test that duplicate username registration fails."""
    driver = get_driver()
    
    try:
        log_test_step("First signup attempt - Creating account")
        navigate_to(driver, "/signup")
        
        username = generate_unique_username()
        password = "testpass123"
        
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        type_text(driver, "input-confirm-password", password)
        click_element(driver, "button-signup-submit")
        
        wait_for_url_contains(driver, "/")
        time.sleep(1)
        
        log_test_step("Clearing session for second attempt")
        clear_session(driver)
        navigate_to(driver, "/signup")
        time.sleep(1)
        
        log_test_step(f"Second signup attempt - Trying duplicate username: {username}")
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        type_text(driver, "input-confirm-password", password)
        
        save_screenshot(driver, "signup_duplicate_before")
        
        click_element(driver, "button-signup-submit")
        time.sleep(2)
        
        error_element = wait_for_element(driver, "alert-signup-error")
        assert error_element.is_displayed(), "Error alert should be visible"
        
        save_screenshot(driver, "signup_duplicate_error")
        print(f"SUCCESS: Duplicate username '{username}' correctly rejected")
        
    finally:
        driver.quit()


def test_signup_password_mismatch():
    """Test that mismatched passwords show error."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/signup")
        
        username = generate_unique_username()
        
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", "password1")
        type_text(driver, "input-confirm-password", "password2")
        
        click_element(driver, "button-signup-submit")
        time.sleep(1)
        
        error_element = wait_for_element(driver, "alert-signup-error")
        assert "match" in error_element.text.lower(), "Error should mention password mismatch"
        
        save_screenshot(driver, "signup_password_mismatch")
        print("SUCCESS: Password mismatch correctly detected")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("\n=== Running Signup Tests ===\n")
    
    print("Test 1: Signup Success")
    test_signup_success()
    
    print("\nTest 2: Duplicate Username")
    test_signup_duplicate_id()
    
    print("\nTest 3: Password Mismatch")
    test_signup_password_mismatch()
    
    print("\n=== All Signup Tests Passed ===\n")
