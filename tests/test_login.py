"""
Selenium tests for user login functionality.
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
    BASE_URL
)


def create_test_user(driver, username: str, password: str):
    """Create a test user via signup."""
    navigate_to(driver, "/signup")
    type_text(driver, "input-username", username)
    type_text(driver, "input-password", password)
    type_text(driver, "input-confirm-password", password)
    click_element(driver, "button-signup-submit")
    wait_for_url_contains(driver, "/")
    time.sleep(1)
    clear_session(driver)


def test_login_success():
    """Test successful login flow."""
    driver = get_driver()
    
    try:
        username = generate_unique_username()
        password = "testpass123"
        
        create_test_user(driver, username, password)
        
        navigate_to(driver, "/login")
        save_screenshot(driver, "login_page")
        
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        
        save_screenshot(driver, "login_form_filled")
        
        click_element(driver, "button-login-submit")
        
        wait_for_url_contains(driver, "/")
        time.sleep(1)
        
        username_element = wait_for_element(driver, "text-username")
        assert username in username_element.text, f"Expected username '{username}' in navbar"
        
        save_screenshot(driver, "login_success")
        print(f"SUCCESS: User '{username}' logged in successfully")
        
    finally:
        driver.quit()


def test_login_wrong_password():
    """Test login with incorrect password."""
    driver = get_driver()
    
    try:
        username = generate_unique_username()
        correct_password = "correctpass"
        wrong_password = "wrongpass"
        
        create_test_user(driver, username, correct_password)
        
        navigate_to(driver, "/login")
        
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", wrong_password)
        
        save_screenshot(driver, "login_wrong_password_before")
        
        click_element(driver, "button-login-submit")
        time.sleep(2)
        
        error_element = wait_for_element(driver, "alert-login-error")
        assert error_element.is_displayed(), "Error alert should be visible"
        
        current_url = driver.current_url
        assert "/login" in current_url, "Should still be on login page"
        
        save_screenshot(driver, "login_wrong_password_error")
        print("SUCCESS: Wrong password correctly rejected")
        
    finally:
        driver.quit()


def test_login_nonexistent_user():
    """Test login with non-existent username."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/login")
        
        type_text(driver, "input-username", "nonexistent_user_12345")
        type_text(driver, "input-password", "somepassword")
        
        click_element(driver, "button-login-submit")
        time.sleep(2)
        
        error_element = wait_for_element(driver, "alert-login-error")
        assert error_element.is_displayed(), "Error alert should be visible"
        
        save_screenshot(driver, "login_nonexistent_user_error")
        print("SUCCESS: Non-existent user correctly rejected")
        
    finally:
        driver.quit()


def test_logout():
    """Test logout functionality."""
    driver = get_driver()
    
    try:
        username = generate_unique_username()
        password = "testpass123"
        
        create_test_user(driver, username, password)
        
        navigate_to(driver, "/login")
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        click_element(driver, "button-login-submit")
        
        wait_for_url_contains(driver, "/")
        time.sleep(1)
        
        save_screenshot(driver, "before_logout")
        
        click_element(driver, "button-user-menu")
        time.sleep(0.5)
        
        click_element(driver, "button-logout")
        time.sleep(1)
        
        login_link = wait_for_element(driver, "link-login")
        assert login_link.is_displayed(), "Login link should be visible after logout"
        
        save_screenshot(driver, "after_logout")
        print("SUCCESS: User logged out successfully")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("\n=== Running Login Tests ===\n")
    
    print("Test 1: Login Success")
    test_login_success()
    
    print("\nTest 2: Wrong Password")
    test_login_wrong_password()
    
    print("\nTest 3: Non-existent User")
    test_login_nonexistent_user()
    
    print("\nTest 4: Logout")
    test_logout()
    
    print("\n=== All Login Tests Passed ===\n")
