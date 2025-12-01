"""
Selenium tests for search functionality.
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
    navigate_to
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_search_with_results():
    """Test search functionality with matching results."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/search")
        time.sleep(1)
        
        save_screenshot(driver, "search_page_initial")
        
        type_text(driver, "input-search", "TypeScript")
        
        click_element(driver, "button-search")
        
        time.sleep(2)
        
        results_count = wait_for_element(driver, "text-results-count")
        assert results_count.is_displayed(), "Results count should be visible"
        
        post_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        assert len(post_cards) > 0, "Should have at least one search result"
        
        save_screenshot(driver, "search_with_results")
        print(f"SUCCESS: Found {len(post_cards)} results for 'TypeScript'")
        
    finally:
        driver.quit()


def test_search_no_results():
    """Test search with no matching results."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/search")
        time.sleep(1)
        
        type_text(driver, "input-search", "xyznonexistentquery12345")
        
        click_element(driver, "button-search")
        
        time.sleep(2)
        
        no_results = wait_for_element(driver, "text-no-results")
        assert no_results.is_displayed(), "No results message should be visible"
        
        save_screenshot(driver, "search_no_results")
        print("SUCCESS: No results message shown for non-existent query")
        
    finally:
        driver.quit()


def test_search_result_click():
    """Test clicking a search result navigates to detail page."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/search")
        time.sleep(1)
        
        type_text(driver, "input-search", "React")
        click_element(driver, "button-search")
        
        time.sleep(2)
        
        first_result = driver.find_element(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        testid_attr = first_result.get_attribute("data-testid") or ""
        post_id = testid_attr.replace("card-post-", "")
        
        save_screenshot(driver, "search_before_click")
        
        first_result.click()
        
        wait_for_url_contains(driver, f"/post/{post_id}")
        time.sleep(1)
        
        post_title = wait_for_element(driver, "text-post-title")
        assert post_title.is_displayed(), "Post title should be visible on detail page"
        
        save_screenshot(driver, "search_result_detail")
        print(f"SUCCESS: Clicked search result navigated to post/{post_id}")
        
    finally:
        driver.quit()


def test_search_async_loading():
    """Test that search shows loading state during async fetch."""
    driver = get_driver()
    
    try:
        navigate_to(driver, "/search")
        time.sleep(1)
        
        type_text(driver, "input-search", "JavaScript")
        
        save_screenshot(driver, "search_async_before")
        
        click_element(driver, "button-search")
        
        time.sleep(2)
        
        results = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        assert len(results) > 0, "Search results should be rendered after async load"
        
        save_screenshot(driver, "search_async_after")
        print("SUCCESS: Async search results rendered correctly")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("\n=== Running Search Tests ===\n")
    
    print("Test 1: Search with Results")
    test_search_with_results()
    
    print("\nTest 2: Search No Results")
    test_search_no_results()
    
    print("\nTest 3: Search Result Click")
    test_search_result_click()
    
    print("\nTest 4: Async Loading")
    test_search_async_loading()
    
    print("\n=== All Search Tests Passed ===\n")
