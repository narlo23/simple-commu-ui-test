"""
Selenium tests for theme toggle functionality.
"""
import time
from utils import (
    get_driver,
    save_screenshot,
    wait_for_element_clickable,
    click_element,
    get_body_class,
    navigate_to
)


def test_theme_toggle():
    """Test dark/light theme toggle functionality."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/")
        time.sleep(1)
        
        initial_class = get_body_class(driver)
        save_screenshot(driver, "theme_initial")
        print(f"Initial body class: '{initial_class}'")
        
        click_element(driver, "button-theme-toggle")
        time.sleep(0.5)
        
        after_first_toggle = get_body_class(driver)
        save_screenshot(driver, "theme_after_first_toggle")
        print(f"After first toggle body class: '{after_first_toggle}'")
        
        assert initial_class != after_first_toggle, "Theme should change after toggle"
        
        click_element(driver, "button-theme-toggle")
        time.sleep(0.5)
        
        after_second_toggle = get_body_class(driver)
        save_screenshot(driver, "theme_after_second_toggle")
        print(f"After second toggle body class: '{after_second_toggle}'")
        
        assert initial_class == after_second_toggle, "Theme should return to initial after double toggle"
        
        print("SUCCESS: Theme toggle works correctly")
        
    finally:
        driver.quit()


def test_theme_persistence():
    """Test that theme preference persists across page navigation."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/")
        time.sleep(1)
        
        initial_class = get_body_class(driver)
        
        click_element(driver, "button-theme-toggle")
        time.sleep(0.5)
        
        after_toggle_class = get_body_class(driver)
        save_screenshot(driver, "theme_before_navigation")
        
        navigate_to(driver, "/search")
        time.sleep(1)
        
        after_navigation_class = get_body_class(driver)
        save_screenshot(driver, "theme_after_navigation")
        
        assert after_toggle_class == after_navigation_class, "Theme should persist after navigation"
        
        print("SUCCESS: Theme persists across navigation")
        
    finally:
        driver.quit()


def test_theme_on_different_pages():
    """Test theme toggle on different pages."""
    driver = get_driver()
    pages = ["/", "/login", "/signup", "/search"]
    
    try:
        for page in pages:
            navigate_to(driver, page)
            time.sleep(1)
            
            before_class = get_body_class(driver)
            
            click_element(driver, "button-theme-toggle")
            time.sleep(0.5)
            
            after_class = get_body_class(driver)
            
            assert before_class != after_class, f"Theme should toggle on {page}"
            
            save_screenshot(driver, f"theme_toggle_{page.replace('/', '_') or 'home'}")
            print(f"SUCCESS: Theme toggle works on {page}")
        
        print("SUCCESS: Theme toggle works on all pages")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("\n=== Running Theme Tests ===\n")
    
    print("Test 1: Theme Toggle")
    test_theme_toggle()
    
    print("\nTest 2: Theme Persistence")
    test_theme_persistence()
    
    print("\nTest 3: Theme on Different Pages")
    test_theme_on_different_pages()
    
    print("\n=== All Theme Tests Passed ===\n")
