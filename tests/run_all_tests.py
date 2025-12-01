"""
Run all Selenium UI automation tests.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

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
    
    print("\n" + "=" * 60)
    print("VANILLA COMMUNITY - SELENIUM UI AUTOMATION TESTS")
    print("=" * 60 + "\n")
    
    for test_name, test_func in all_tests:
        print(f"\nRunning: {test_name}")
        print("-" * 40)
        
        try:
            test_func()
            tests_passed += 1
            print(f"PASSED: {test_name}")
        except Exception as e:
            tests_failed += 1
            failed_tests.append((test_name, str(e)))
            print(f"FAILED: {test_name}")
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"\nTotal Tests: {tests_passed + tests_failed}")
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    
    if failed_tests:
        print("\nFailed Tests:")
        for name, error in failed_tests:
            print(f"  - {name}: {error}")
    
    print("\n" + "=" * 60 + "\n")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
