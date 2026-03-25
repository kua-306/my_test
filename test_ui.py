import os
from playwright.sync_api import Page, expect
import random
import re

num = random.randint(0, 9999)
username = f'account{num}'
password = 'password'
def test_example(page: Page) -> None:
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(current_dir, "index.html")
    # page.goto(f'file://{file_path}')
    page.goto(f'file://{os.getcwd()}/index.html')
    expect(page.locator("#auth-section")).to_be_visible()
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Đăng ký").click()
    page.get_by_role("button", name="Đăng nhập").click()
    expect(page.locator("#question-section")).not_to_have_class(re.compile(r"pointer-events-none"))
    page.get_by_role("textbox", name="Câu hỏi").click()
    page.get_by_role("textbox", name="Câu hỏi").fill("hello")
    page.get_by_role("textbox", name="Câu trả lời").click()
    page.get_by_role("textbox", name="Câu trả lời").fill("hi")
    page.get_by_role("button", name="Gửi câu hỏi").click()
    expect(page.get_by_text("Câu hỏi đã được tạo!")).to_be_visible()
    

