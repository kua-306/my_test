import pytest
from playwright.sync_api import Page, expect

import random

@pytest.fixture
def api_page(page: Page):
    # Tạo username ngẫu nhiên để không bao giờ bị trùng
    rand_id = random.randint(1000, 9999)
    username = f"user_{rand_id}"
    password = "password123"
    payload = f'{{"username": "{username}", "password": "{password}"}}'
    
    page.goto('http://127.0.0.1:8000/docs')
    
    # --- BƯỚC 1: ĐĂNG KÝ (Bắt buộc phải đợi Response) ---
    signup_section = page.locator("#operations-default-create_user_create_user__post")
    signup_section.click()
    signup_section.get_by_role("button", name="Try it out").click()
    signup_section.locator("textarea.body-param__text").fill(payload)
    
    with page.expect_response("**/create-user/", timeout=5000) as signup_res:
        signup_section.get_by_role("button", name="Execute").click()
    
    # Nếu đăng ký thất bại, in ra lỗi để soi
    if signup_res.value.status not in [200, 201]:
        print(f"SIGNUP FAILED: {signup_res.value.json()}")
        
    signup_section.click() 

    # --- BƯỚC 2: ĐĂNG NHẬP ---
    login_section = page.locator("#operations-default-login_login__post")
    login_section.click()
    login_section.get_by_role("button", name="Try it out").click()
    login_section.locator("textarea.body-param__text").fill(payload)

    with page.expect_response("**/login/", timeout=5000) as login_res:
        login_section.get_by_role("button", name="Execute").click()
    
    resp_json = login_res.value.json()
    
    # Bắt lỗi 400 tại đây và in ra chi tiết nhất có thể
    if 'access_token' not in resp_json:
        print(f"LOGIN FAILED. Status: {login_res.value.status}")
        print(f"Payload sent: {payload}")
        print(f"API Response: {resp_json}")
        raise KeyError(f"Login Error: {resp_json.get('detail', 'No detail')}")

    token = resp_json['access_token']
    page.set_extra_http_headers({"Authorization": f"Bearer {token}"})
    
    login_section.click()
    return page
@pytest.fixture
def create_question(api_page):    
    section = api_page.locator("#operations-default-create_question_create_question__post")
    section.click()
    section.get_by_role("button", name="Try it out").click()
    section.locator("textarea.body-param__text").fill(
        '{"question": "Python?", "options": ["Ngôn ngữ", "Con rắn"], "answer": "Ngôn ngữ"}'
    )
    
    # CHỈ NHẤN EXECUTE 1 LẦN TRONG KHỐI WITH
    # Dùng section để tránh bị trùng với các nút Execute khác
    with api_page.expect_response("**/create-question/") as response_info:
        section.get_by_role("button", name="Execute").click()
    
    response = response_info.value
    assert response.status == 201 or response.status == 200 # Tùy Backend trả về
    return response.json()['id']

def test_get_question(api_page, create_question):
    question_id = str(create_question) 
    
    section = api_page.locator("#operations-default-get_question_get_question__question_id__get")
    section.click()
    section.get_by_role("button", name="Try it out").click()
    
    # Điền ID lấy từ fixture
    section.get_by_role("textbox", name="question_id").fill(question_id)
    section.get_by_role("button", name="Execute").click()
    expect(section.locator(".response-col_description pre").first).to_contain_text(question_id)

def test_patch(api_page, create_question):
    question_id = str(create_question)
    section= api_page.locator("#operations-default-update_question_update_question__question_id__patch")
    section.click()
    section.get_by_role("button", name="Try it out").click()
    section.get_by_role("textbox", name="question_id").fill(question_id)
    section.locator("textarea.body-param__text").fill(
        '{"question": "what is python?","answer": "Ngôn ngữ"}'
    )
    section.get_by_role("button", name="Execute").click()
    expect(section.locator(".response-col_description pre").first).to_contain_text(question_id)

def test_delete(api_page, create_question):
    question_id = str(create_question)
    section = api_page.locator("#operations-default-delete_question_delete_question__question_id__delete")
    section.click()
    section.get_by_role("button", name="Try it out").click()
    section.get_by_role("textbox", name="question_id").fill(question_id)
    section.get_by_role("button", name="Execute").click()
    expect(section.get_by_text("Question deleted successfully")).to_be_visible()