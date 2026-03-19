import os
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(current_dir, "index.html")
    # page.goto(f'file://{file_path}')
    page.goto(f'file://{os.getcwd()}/index.html')
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("thune")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("ntltcua3006")
    page.get_by_role("button", name="Đăng ký").click()
    page.get_by_role("button", name="Đăng ký").click()
    page.get_by_role("button", name="Đăng ký").click()
    page.get_by_role("button", name="Đăng nhập").click()
    page.get_by_role("textbox", name="Câu hỏi").click()
    page.get_by_role("textbox", name="Câu hỏi").fill("hello")
    page.get_by_role("textbox", name="Câu trả lời").click()
    page.get_by_role("textbox", name="Câu trả lời").click()
    page.get_by_role("textbox", name="Câu trả lời").fill("hi")
    page.get_by_role("button", name="Gửi câu hỏi").click()
