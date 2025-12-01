"""
종합 통합 테스트 - 회원가입부터 검색까지 모든 기능을 한 번에 테스트합니다.
학생 수준을 고려한 간단하고 읽기 쉬운 코드입니다.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ==================== 설정 ====================
BASE_URL = "http://localhost:5000"
HEADLESS = False  # True로 설정하면 브라우저 창이 안 보임

# 로그 출력 함수
def print_log(title, message):
    """로그를 보기 좋게 출력합니다."""
    print(f"\n{'='*60}")
    print(f"[{title}] {message}")
    print(f"{'='*60}\n")

def print_step(step_num, description):
    """각 단계를 표시합니다."""
    print(f"  Step {step_num}: {description}...")

def print_success(text):
    """성공을 표시합니다."""
    print(f"  ✓ 성공: {text}")

def print_failure(text):
    """실패를 표시합니다."""
    print(f"  ✗ 실패: {text}")


# ==================== 드라이버 설정 ====================
def create_driver():
    """크롬 드라이버를 생성합니다."""
    options = Options()
    
    if HEADLESS:
        options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver


# ==================== 도움 함수 ====================
def find_by_testid(driver, testid):
    """data-testid 속성으로 요소를 찾습니다."""
    return driver.find_element(By.CSS_SELECTOR, f'[data-testid="{testid}"]')

def click_element(driver, testid):
    """요소를 클릭합니다."""
    element = find_by_testid(driver, testid)
    element.click()
    return element

def type_text(driver, testid, text):
    """텍스트를 입력합니다."""
    element = find_by_testid(driver, testid)
    element.clear()
    element.send_keys(text)
    return element

def get_page_title(driver):
    """현재 페이지의 제목을 가져옵니다."""
    return driver.title


# ==================== 테스트 함수 ====================
def test_comprehensive_flow():
    """
    모든 기능을 한 번에 테스트하는 통합 테스트입니다.
    한 번에 브라우저를 닫지 않고 계속 진행합니다.
    """
    
    print_log("통합 테스트 시작", "회원가입 → 로그인 → 게시글 확인 → 검색 → 테마 변경")
    
    driver = create_driver()
    
    try:
        # ========== 1단계: 회원가입 ==========
        print("\n" + "="*60)
        print("📝 1단계: 회원가입 테스트")
        print("="*60)
        
        print_step(1, "회원가입 페이지로 이동")
        driver.get(f"{BASE_URL}/signup")
        time.sleep(1)
        print_success("회원가입 페이지 로드됨")
        
        # 테스트용 사용자명 생성 (현재 시간 기반)
        username = f"testuser_{int(time.time() * 1000)}"
        password = "testpass123"
        
        print_step(2, f"회원가입 양식 작성 (username: {username})")
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        type_text(driver, "input-confirm-password", password)
        time.sleep(0.5)
        print_success("양식 작성 완료")
        
        print_step(3, "회원가입 버튼 클릭")
        click_element(driver, "button-signup-submit")
        time.sleep(2)  # 회원가입 처리 대기
        print_success("회원가입 완료")
        
        # 회원가입 확인
        username_element = find_by_testid(driver, "text-username")
        assert username in username_element.text, "사용자명이 화면에 표시되어야 합니다"
        print_success(f"네비게이션에 사용자명 '{username}' 확인됨")
        
        
        # ========== 2단계: 로그아웃 ==========
        print("\n" + "="*60)
        print("🔓 2단계: 로그아웃 테스트")
        print("="*60)
        
        print_step(1, "사용자 메뉴 드롭다운 열기")
        click_element(driver, "button-user-menu")
        time.sleep(0.5)
        print_success("드롭다운 메뉴 열림")
        
        print_step(2, "로그아웃 버튼 클릭")
        click_element(driver, "button-logout")
        time.sleep(1.5)
        print_success("로그아웃 완료")
        
        # 로그아웃 확인
        try:
            find_by_testid(driver, "text-username")
            print_failure("사용자명이 여전히 표시됨 - 로그아웃 실패")
        except:
            print_success("사용자명이 제거됨 - 로그아웃 확인됨")
        
        
        # ========== 3단계: 로그인 ==========
        print("\n" + "="*60)
        print("🔐 3단계: 로그인 테스트")
        print("="*60)
        
        print_step(1, "로그인 페이지로 이동")
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        print_success("로그인 페이지 로드됨")
        
        print_step(2, f"로그인 양식 작성 (username: {username})")
        type_text(driver, "input-username", username)
        type_text(driver, "input-password", password)
        time.sleep(0.5)
        print_success("양식 작성 완료")
        
        print_step(3, "로그인 버튼 클릭")
        click_element(driver, "button-login-submit")
        time.sleep(2)  # 로그인 처리 대기
        print_success("로그인 완료")
        
        # 로그인 확인
        username_element = find_by_testid(driver, "text-username")
        assert username in username_element.text, "로그인 후 사용자명이 표시되어야 합니다"
        print_success(f"네비게이션에 사용자명 '{username}' 확인됨")
        
        
        # ========== 4단계: 랜딩 페이지 확인 ==========
        print("\n" + "="*60)
        print("🏠 4단계: 랜딩 페이지 확인")
        print("="*60)
        
        print_step(1, "홈 페이지로 이동")
        driver.get(f"{BASE_URL}/")
        time.sleep(1.5)
        print_success("홈 페이지 로드됨")
        
        print_step(2, "최근 게시글 5개가 표시되었는지 확인")
        # 게시글 카드를 찾습니다 (data-testid가 "card-post-"로 시작)
        posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        assert len(posts) >= 5, f"최소 5개의 게시글이 필요한데 {len(posts)}개만 있습니다"
        print_success(f"{len(posts)}개의 게시글이 표시됨")
        
        # 각 게시글 제목 출력
        for i, post in enumerate(posts[:5], 1):
            try:
                # data-testid="text-post-title" 속성으로 제목 찾기
                title_elem = post.find_element(By.CSS_SELECTOR, '[data-testid^="text-post-"]')
                title = title_elem.text
            except:
                # 실패하면 h2나 다른 헤더 태그 시도
                try:
                    title = post.find_element(By.TAG_NAME, "h2").text
                except:
                    title = "제목 없음"
            print(f"    - {i}번 게시글: {title[:40]}...")
        
        
        # ========== 5단계: 게시글 상세페이지 ==========
        print("\n" + "="*60)
        print("📄 5단계: 게시글 상세페이지 테스트")
        print("="*60)
        
        print_step(1, "첫 번째 게시글 클릭")
        first_post = posts[0]
        first_post_testid = first_post.get_attribute("data-testid") or ""
        first_post_id = first_post_testid.replace("card-post-", "")
        first_post.click()
        time.sleep(1.5)
        print_success("게시글 상세페이지 로드됨")
        
        # 상세페이지 확인
        post_title = find_by_testid(driver, "text-post-title")
        assert post_title.is_displayed(), "게시글 제목이 표시되어야 합니다"
        print_success(f"게시글 제목: {post_title.text}")
        
        
        # ========== 6단계: 이전 페이지로 돌아가기 ==========
        print("\n" + "="*60)
        print("⬅️  6단계: 뒤로 가기 테스트")
        print("="*60)
        
        print_step(1, "뒤로 가기 버튼 클릭")
        driver.back()
        time.sleep(1)
        print_success("홈 페이지로 돌아옴")
        
        # 홈 페이지 확인
        posts_after_back = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        assert len(posts_after_back) >= 5, "홈 페이지의 게시글 목록이 표시되어야 합니다"
        print_success("게시글 목록이 다시 표시됨")
        
        
        # ========== 7단계: 검색 기능 ==========
        print("\n" + "="*60)
        print("🔍 7단계: 검색 기능 테스트")
        print("="*60)
        
        print_step(1, "검색 페이지로 이동")
        driver.get(f"{BASE_URL}/search")
        time.sleep(1)
        print_success("검색 페이지 로드됨")
        
        print_step(2, "검색어 입력 (검색어: 'React')")
        type_text(driver, "input-search", "React")
        time.sleep(0.5)
        print_success("검색어 입력 완료")
        
        print_step(3, "검색 버튼 클릭")
        click_element(driver, "button-search")
        time.sleep(1.5)  # 검색 결과 로드 대기
        print_success("검색 실행 완료")
        
        # 검색 결과 확인
        search_results = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
        assert len(search_results) > 0, "검색 결과가 1개 이상이어야 합니다"
        print_success(f"검색 결과: {len(search_results)}개의 게시글이 검색됨")
        
        # 검색 결과 확인
        for i, result in enumerate(search_results, 1):
            try:
                # data-testid="text-post-title" 속성으로 제목 찾기
                title_elem = result.find_element(By.CSS_SELECTOR, '[data-testid^="text-post-title-"]')
                title = title_elem.text
            except:
                # 실패하면 h2 시도
                try:
                    title = result.find_element(By.TAG_NAME, "h2").text
                except:
                    title = "제목 없음"
            print(f"    - {i}번 결과: {title[:40]}...")
        
        print_step(4, "검색 결과가 'React' 키워드를 포함하는지 확인")
        all_contain_keyword = all(
            "react" in result.text.lower() 
            for result in search_results
        )
        assert all_contain_keyword, "모든 검색 결과가 검색어를 포함해야 합니다"
        print_success("모든 검색 결과가 'React' 키워드를 포함함")
        
        
        # ========== 8단계: 테마 전환 ==========
        print("\n" + "="*60)
        print("🌙 8단계: 테마 전환 테스트")
        print("="*60)
        
        print_step(1, "홈 페이지로 이동")
        driver.get(f"{BASE_URL}/")
        time.sleep(1)
        print_success("홈 페이지 로드됨")
        
        # 초기 테마 확인
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_theme = html_element.get_attribute("class")
        print_step(2, f"초기 테마 확인 (class: {initial_theme})")
        print_success(f"초기 테마: {initial_theme if initial_theme else '라이트 모드'}")
        
        print_step(3, "테마 토글 버튼 클릭")
        click_element(driver, "button-theme-toggle")
        time.sleep(1)
        print_success("테마 전환 완료")
        
        # 테마 변경 확인
        new_theme = html_element.get_attribute("class")
        assert initial_theme != new_theme, "테마가 변경되어야 합니다"
        print_success(f"테마 변경됨: {initial_theme} → {new_theme}")
        
        print_step(4, "다시 테마 토글 버튼 클릭")
        click_element(driver, "button-theme-toggle")
        time.sleep(1)
        print_success("테마 복원 완료")
        
        # 초기 테마로 복원 확인
        restored_theme = html_element.get_attribute("class")
        assert initial_theme == restored_theme, "테마가 원래대로 복원되어야 합니다"
        print_success(f"테마 복원됨: {restored_theme}")
        
        
        # ========== 9단계: 로그아웃 후 테마 확인 ==========
        print("\n" + "="*60)
        print("🌙 9단계: 로그아웃 후 테마 테스트")
        print("="*60)
        
        print_step(1, "현재 테마 저장")
        current_theme = html_element.get_attribute("class")
        print_success(f"현재 테마: {current_theme if current_theme else '라이트 모드'}")
        
        print_step(2, "사용자 메뉴 드롭다운 열기")
        click_element(driver, "button-user-menu")
        time.sleep(0.5)
        print_success("드롭다운 메뉴 열림")
        
        print_step(3, "로그아웃 버튼 클릭")
        click_element(driver, "button-logout")
        time.sleep(1.5)
        print_success("로그아웃 완료")
        
        print_step(4, "로그아웃 후 테마 확인")
        theme_after_logout = html_element.get_attribute("class")
        print_success(f"로그아웃 후 테마: {theme_after_logout if theme_after_logout else '라이트 모드'}")
        
        print_step(4, "테마가 유지되었는지 확인")
        assert current_theme == theme_after_logout, "테마가 유지되어야 합니다 (localStorage)"
        print_success("테마가 올바르게 유지됨")
        
        
        # ========== 최종 결과 ==========
        print("\n" + "="*60)
        print("✅ 모든 테스트 성공!")
        print("="*60)
        print("""
        테스트 완료 항목:
        ✓ 회원가입
        ✓ 로그아웃
        ✓ 로그인
        ✓ 랜딩 페이지 (5개 게시글 확인)
        ✓ 게시글 상세페이지
        ✓ 뒤로 가기
        ✓ 검색 기능
        ✓ 테마 전환
        ✓ 로그아웃 후 테마 유지
        """)
        print("="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print_failure(f"테스트 중 오류 발생")
        print("="*60)
        print(f"오류: {str(e)}\n")
        raise
        
    finally:
        # 테스트 끝 - 브라우저 종료
        print("브라우저를 닫고 있습니다...")
        time.sleep(1)
        driver.quit()


# ==================== 실행 ====================
if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  종합 통합 테스트 - Vanilla Community Platform".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    test_comprehensive_flow()
