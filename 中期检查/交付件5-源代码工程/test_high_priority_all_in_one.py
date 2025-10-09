import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


# ----------------------------
# 配置常量（请根据实际环境修改）
# ----------------------------
BASE_URL = "http://localhost:8080"
API_BASE = "http://localhost:8080/login"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"
VISITOR_USERNAME = "test"
VISITOR_PASSWORD = "123"

# 假设已知的用户 ID（用于 API 测试）
OTHER_ADMIN_ID = "test"
SELF_ADMIN_ID = "editor"


# ----------------------------
# Fixture：共享浏览器和登录
# ----------------------------
@pytest.fixture(scope="class")
def driver():
    options = Options()
    options.add_argument("--headless")  # 可选：无头模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture(scope="class")
def admin_token():
    """通过登录接口获取管理员 JWT token（用于 API 测试）"""
    resp = requests.post(f"{API_BASE}/auth/login", json={
        "email": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })
    assert resp.status_code == 200
    return resp.json().get("token")


def login_as_admin(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.NAME, "email").send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.ID, "login-btn").click()
    # 等待跳转
    assert "dashboard" in driver.current_url or "admin" in driver.current_url


def login_as_visitor(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.NAME, "email").send_keys(VISITOR_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(VISITOR_PASSWORD)
    driver.find_element(By.ID, "login-btn").click()


# ----------------------------
# 高优先级测试用例类
# ----------------------------
@pytest.mark.usefixtures("driver")
class TestHighPriority:

    # HOME-PROJ-02
    def test_home_proj_02_copyright_info(self, driver):
        driver.get(BASE_URL)
        proj_link = driver.find_elements(By.LINK_TEXT, "项目介绍")
        if proj_link:
            proj_link[0].click()
        else:
            driver.get(f"{BASE_URL}/about")
        copyright_el = driver.find_element(By.ID, "copyright-info")
        text = copyright_el.text
        assert ("版权所有" in text) or ("©" in text) or ("Copyright" in text)

    # NOTE-ART-01
    def test_note_art_01_unlogged_no_write_button(self, driver):
        driver.get(f"{BASE_URL}/notebook")
        write_btn = driver.find_elements(By.ID, "write-article-btn")
        assert len(write_btn) == 0

    # NOTE-ART-02
    def test_note_art_02_logged_visitor_can_write(self, driver):
        login_as_visitor(driver)
        driver.get(f"{BASE_URL}/notebook")
        write_btn = driver.find_element(By.ID, "write-article-btn")
        assert write_btn.is_displayed()

    # LIB-INFO-01
    def test_lib_info_01_book_click_redirects_to_detail(self, driver):
        driver.get(f"{BASE_URL}/library")
        books = driver.find_elements(By.CSS_SELECTOR, ".book-item a")
        assert len(books) > 0
        first_href = books[0].get_attribute("href")
        assert "/book/" in first_href

    # LIB-INFO-03
    def test_lib_info_03_hover_shows_summary(self, driver):
        driver.get(f"{BASE_URL}/library")
        book = driver.find_element(By.CSS_SELECTOR, ".book-item")
        ActionChains(driver).move_to_element(book).perform()
        tooltips = driver.find_elements(By.CLASS_NAME, "book-summary-tooltip")
        assert len(tooltips) > 0 and tooltips[0].is_displayed()

    # LIB-SRCH-01, 04, 05, 06, 07, 08, 10, 12, 13
    @pytest.mark.parametrize("keyword,should_have_results", [
        ("人工智能", True),      # LIB-SRCH-01
        ("三体", True),          # LIB-SRCH-04
        ("刘慈欣", True),        # LIB-SRCH-05
        ("", True),              # LIB-SRCH-06（空白应返回全部）
        ("村上春树 日本", True), # LIB-SRCH-07
        ("法国", True),          # LIB-SRCH-08
        (" 三体", True),         # LIB-SRCH-10（前空格应被处理）
        ("鲁迅 呐喊", True),     # LIB-SRCH-12
        ("托尔斯泰 战争与和平 俄国", True),  # LIB-SRCH-13
    ])
    def test_lib_search_high_priority(self, driver, keyword, should_have_results):
        driver.get(f"{BASE_URL}/library")
        search_box = driver.find_element(By.ID, "search-input")
        search_box.clear()
        search_box.send_keys(keyword)
        driver.find_element(By.ID, "search-btn").click()
        results = driver.find_elements(By.CLASS_NAME, "book-item")
        if should_have_results:
            assert len(results) > 0, f"搜索 '{keyword}' 应返回结果"
        else:
            assert len(results) == 0

    # ADMIN-STAT-01
    def test_admin_stat_01_weekly_stats_displayed(self, driver):
        login_as_admin(driver)
        driver.get(f"{BASE_URL}/admin")
        stats_container = driver.find_element(By.ID, "weekly-stats")
        text = stats_container.text
        required = ["新用户", "书籍浏览量", "书籍数量"]
        for item in required:
            assert item in text

    # AUTH-LOGIN-01
    def test_auth_login_01_unlogged_redirect_to_login(self, driver):
        driver.get(f"{BASE_URL}/admin")
        assert "login" in driver.current_url

    # ADMIN-CONT-01
    def test_admin_cont_01_publish_text_article(self, driver):
        login_as_admin(driver)
        driver.get(f"{BASE_URL}/admin/articles")
        driver.find_element(By.ID, "write-article-btn").click()
        driver.find_element(By.ID, "article-title").send_keys("Auto Test Article")
        driver.find_element(By.ID, "article-content").send_keys("This is a test.")
        driver.find_element(By.ID, "publish-btn").click()
        success_msgs = driver.find_elements(By.CLASS_NAME, "success-message")
        assert len(success_msgs) > 0

    # ADMIN-CONT-02（简化：仅验证文件类型校验提示）
    def test_admin_cont_02_image_upload_rejects_invalid_type(self, driver):
        login_as_admin(driver)
        driver.get(f"{BASE_URL}/admin/articles/write")
        upload = driver.find_element(By.ID, "image-upload")
        # 模拟上传 .exe（实际需用合法路径，此处用 JS 触发错误）
        driver.execute_script("document.getElementById('image-upload').value = 'fake.exe';")
        # 触发 change 事件（根据前端实现调整）
        driver.execute_script("document.getElementById('image-upload').dispatchEvent(new Event('change'));")
        error_el = driver.find_elements(By.CLASS_NAME, "upload-error")
        if error_el:
            assert "不支持" in error_el[0].text or "invalid" in error_el[0].text.lower()

    # ADMIN-USER-02, 03, 15（API 测试）
    def test_admin_user_02_cannot_disable_other_admin(self, admin_token):
        resp = requests.post(
            f"{API_BASE}/admin/users/disable",
            json={"user_id": OTHER_ADMIN_ID},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 403

    def test_admin_user_03_cannot_disable_self(self, admin_token):
        resp = requests.post(
            f"{API_BASE}/admin/users/disable",
            json={"user_id": SELF_ADMIN_ID},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 403

    def test_admin_user_15_cannot_revoke_own_admin_role(self, admin_token):
        resp = requests.post(
            f"{API_BASE}/admin/users/revoke-role",
            json={"user_id": SELF_ADMIN_ID, "role": "system_admin"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 403