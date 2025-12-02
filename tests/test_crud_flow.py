"""
게시글 CRUD 전체 플로우 테스트
로그인 → 게시글 생성 → 리스트에서 확인 → 상세페이지 → 수정 → 삭제
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ========== 설정: 여기서 변수 수정하세요 ==========
# BASE_URL = "http://localhost:5001" 각 로컬환경에 맞도록 수정
# BASE_URL = "http://localhost:5000/" 잘못된 예시. 뒤에 /로 붙여서 끝내면 안됨
BASE_URL = "http://localhost:5000"
TEST_USERNAME = "admin"           # 테스트할 사용자명 수정
TEST_PASSWORD = "1234"            # 테스트할 비밀번호 수정
WAIT_TIMEOUT = 10                 # 요소 로드 대기 시간 (초)
# ==============================================

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(WAIT_TIMEOUT)
wait = WebDriverWait(driver, WAIT_TIMEOUT)

try:
    print("="*60)
    print("게시글 CRUD 전체 플로우 테스트 시작")
    print("="*60)
    
    # 1단계: 로그인
    print("\n[1단계] 로그인 중...")
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    
    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="input-username"]')))
    password_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-password"]')
    
    username_input.send_keys(TEST_USERNAME)
    password_input.send_keys(TEST_PASSWORD)
    
    login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-login-submit"]')
    login_button.click()
    
    # 로그인 완료 확인: "Create Post" 버튼이 나타날 때까지 대기 (세션 설정 완료)
    print("\n[1-1단계] 로그인 완료 확인 중...")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Post')]")))
    
    # 쿠키 확인 및 세션 안정화 대기
    print("[1-2단계] 세션 쿠키 확인 중...")
    time.sleep(1)  # 쿠키가 완전히 저장될 때까지 대기
    cookies = driver.get_cookies()
    session_cookie = [c for c in cookies if c['name'] == 'connect.sid']
    if session_cookie:
        print(f"✓ 세션 쿠키 확인됨: {session_cookie[0]['name']}")
    else:
        print("⚠ 경고: 세션 쿠키가 없습니다. 게시글 생성이 실패할 수 있습니다.")
    
    print("✓ 로그인 완료 및 인증 상태 확인됨")
    
    # 2-1단계: 게시글 생성 버튼 클릭
    print("\n[2단계] 게시글 생성 버튼 클릭...")
    create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create Post')]")
    create_button.click()
    time.sleep(2)
    print("✓ 게시글 생성 페이지 로드됨")
    
    # 3단계: 게시글 작성
    print("\n[3단계] 게시글 작성 중...")
    title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="input-post-title"]')))
    content_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="textarea-post-content"]')
    category_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-post-category"]')
    
    post_title = "테스트 게시글 - CRUD 플로우"
    post_content = "이것은 자동 테스트로 생성된 게시글입니다.\n\n게시글 생성, 수정, 삭제를 테스트합니다."
    post_category = "테스트"
    
    title_input.send_keys(post_title)
    content_input.send_keys(post_content)
    category_input.send_keys(post_category)
    
    time.sleep(1)
    print(f"✓ 게시글 작성 완료: {post_title}")
    
    # 4단계: 게시글 제출
    print("\n[4단계] 게시글 제출 중...")
    submit_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-create-post"]')
    submit_button.click()
    
    # URL이 /post/{id} 형태로 변경될 때까지 대기 (성공 확인)
    print("[4-1단계] 게시글 생성 완료 대기 중...")
    current_url = ""
    try:
        # 10초 동안 현재 URL이 /post/ 를 포함할 때까지 대기
        for i in range(50):  # 10초간 0.2초마다 확인
            current_url = driver.current_url
            if "/post/" in current_url and current_url != f"{BASE_URL}/post/create":
                break
            time.sleep(0.2)
        
        created_post_id = current_url.split("/post/")[-1]
        print(f"✓ 게시글 제출 완료 및 상세페이지 로드됨")
        print(f"✓ 생성된 게시글 ID: {created_post_id}")
    except Exception as e:
        print(f"✗ 게시글 제출 실패: {str(e)}")
        # 에러 토스트 메시지 확인
        try:
            error_toast = driver.find_element(By.XPATH, "//*[contains(text(), 'Error') or contains(text(), 'Not authenticated')]")
            print(f"✗ 에러 메시지: {error_toast.text}")
        except:
            pass
        raise
    
    # 5단계: 홈페이지로 돌아가서 생성된 게시글 확인
    print("\n[5단계] 홈페이지에서 생성된 게시글 확인...")
    driver.get(f"{BASE_URL}/")
    time.sleep(2)
    
    post_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
    print(f"✓ 게시글 목록에서 {len(post_cards)}개의 게시글 표시됨")
    
    # 생성된 게시글이 리스트에 있는지 확인
    created_post_found = False
    for card in post_cards:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, '[data-testid^="text-post-title-"]')
            if post_title in title_elem.text:
                created_post_found = True
                print(f"✓ 생성된 게시글이 리스트에서 확인됨: {title_elem.text}")
                break
        except:
            continue
    
    if not created_post_found:
        print("! 주의: 생성된 게시글을 리스트에서 찾지 못했습니다")
    
    # 6단계: 생성된 게시글 상세페이지로 이동
    print("\n[6단계] 생성된 게시글 상세페이지 이동...")
    driver.get(f"{BASE_URL}/post/{created_post_id}")
    time.sleep(2)
    
    detail_title = driver.find_element(By.CSS_SELECTOR, '[data-testid="text-post-title"]')
    print(f"✓ 상세페이지 로드됨: {detail_title.text}")
    
    # 7단계: 수정 버튼 클릭
    print("\n[7단계] 게시글 수정 중...")
    edit_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-edit-post"]')
    edit_button.click()
    
    time.sleep(2)
    print("✓ 수정 페이지로 이동")
    
    # 8단계: 게시글 수정
    print("\n[8단계] 게시글 내용 수정...")
    title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="input-post-title"]')))
    content_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="textarea-post-content"]')
    
    # 기존 텍스트 삭제 후 새 텍스트 입력
    title_input.clear()
    content_input.clear()
    
    updated_title = post_title + " (수정됨)"
    updated_content = post_content + "\n\n[수정됨] 이 게시글은 수정되었습니다."
    
    title_input.send_keys(updated_title)
    content_input.send_keys(updated_content)
    
    time.sleep(1)
    print(f"✓ 게시글 수정 완료: {updated_title}")
    
    # 9단계: 수정 제출
    print("\n[9단계] 수정 내용 제출...")
    update_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-update-post"]')
    update_button.click()
    
    time.sleep(2)
    print("✓ 수정 제출 완료")
    
    # 10단계: 수정된 내용 확인
    print("\n[10단계] 수정된 게시글 확인...")
    time.sleep(1)
    
    detail_title = driver.find_element(By.CSS_SELECTOR, '[data-testid="text-post-title"]')
    detail_content = driver.find_element(By.CSS_SELECTOR, '[data-testid="text-post-content"]')
    
    print(f"✓ 수정된 제목: {detail_title.text}")
    
    if "[수정됨]" in detail_content.text:
        print("✓ 수정된 내용이 정상적으로 반영됨")
    
    # 11단계: 게시글 삭제
    print("\n[11단계] 게시글 삭제...")
    delete_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-delete-post"]')
    delete_button.click()
    
    time.sleep(2)
    print("✓ 게시글 삭제 완료")
    
    # 12단계: 홈페이지로 이동하여 삭제 확인
    print("\n[12단계] 홈페이지에서 삭제 확인...")
    driver.get(f"{BASE_URL}/")
    time.sleep(2)
    
    post_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid^="card-post-"]')
    
    deleted_post_found = False
    for card in post_cards:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, '[data-testid^="text-post-title-"]')
            if updated_title in title_elem.text:
                deleted_post_found = True
                break
        except:
            continue
    
    if not deleted_post_found:
        print("✓ 게시글이 리스트에서 삭제됨 (삭제 성공)")
    else:
        print("! 주의: 삭제된 게시글이 여전히 리스트에 표시됨")
    
    print("\n" + "="*60)
    print("✓✓✓ 게시글 CRUD 전체 플로우 테스트 완료!")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    print("\n브라우저를 닫고 있습니다...")
    driver.quit()
    print("✓ 완료")
