"""
Run all Selenium UI automation tests.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from utils import logger, log_test_success, log_test_failure
from test_signup import (
    test_signup_success,
    test_signup_duplicate_id,
    test_signup_password_mismatch
)
from test_login import (
    test_login_success,
    test_login_wrong_password,
    test_login_nonexistent_user,
    test_logout
)
from test_theme import (
    test_theme_toggle,
    test_theme_persistence,
    test_theme_on_different_pages
)
from test_search import (
    test_search_with_results,
    test_search_no_results,
    test_search_result_click,
    test_search_async_loading
)


def run_all_tests():
    """Run all test suites."""
    tests_passed = 0
    tests_failed = 0
    failed_tests = []
    
    all_tests = [
        ("Signup - Success", test_signup_success),
        ("Signup - Duplicate ID", test_signup_duplicate_id),
        ("Signup - Password Mismatch", test_signup_password_mismatch),
        ("Login - Success", test_login_success),
        ("Login - Wrong Password", test_login_wrong_password),
        ("Login - Non-existent User", test_login_nonexistent_user),
        ("Login - Logout", test_logout),
        ("Theme - Toggle", test_theme_toggle),
        ("Theme - Persistence", test_theme_persistence),
        ("Theme - Different Pages", test_theme_on_different_pages),
        ("Search - With Results", test_search_with_results),
        ("Search - No Results", test_search_no_results),
        ("Search - Result Click", test_search_result_click),
        ("Search - Async Loading", test_search_async_loading),
    ]
    
    logger.info("\n" + "=" * 70)
    logger.info("🚀 VANILLA COMMUNITY - SELENIUM UI AUTOMATION TEST SUITE")
    logger.info("=" * 70)
    logger.info(f"Total Tests to Run: {len(all_tests)}\n")
    
    start_time = time.time()
    
    for idx, (test_name, test_func) in enumerate(all_tests, 1):
        test_start = time.time()
        logger.info(f"\n[{idx}/{len(all_tests)}] Running: {test_name}")
        logger.info("-" * 70)
        
        try:
            test_func()
            duration = time.time() - test_start
            tests_passed += 1
            log_test_success(test_name, duration)
        except Exception as e:
            duration = time.time() - test_start
            tests_failed += 1
            failed_tests.append((test_name, str(e)))
            log_test_failure(test_name, str(e), duration)
    
    total_duration = time.time() - start_time
    
    logger.info("\n" + "=" * 70)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total Tests: {tests_passed + tests_failed}")
    logger.info(f"✓ Passed: {tests_passed}")
    logger.info(f"✗ Failed: {tests_failed}")
    logger.info(f"⏱️  Total Duration: {total_duration:.2f}s")
    
    if failed_tests:
        logger.info("\n❌ Failed Tests Details:")
        for name, error in failed_tests:
            logger.info(f"  - {name}")
            logger.info(f"    Error: {error}")
    else:
        logger.info("\n✅ All tests passed successfully!")
    
    logger.info("\n" + "=" * 70 + "\n")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
