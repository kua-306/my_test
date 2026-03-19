import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("file:///C:/Users/thuu/Documents/FastAPI/tutorial/quizz/index.html")
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
