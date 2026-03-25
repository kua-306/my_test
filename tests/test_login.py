from pages.login_page import LoginPage
from pages.question_page import QuestionPage
import pytest
import random
from playwright.sync_api import Page, expect

num = random.randint(0, 9999)
username = f'account{num}'
password = 'password'
def test_login():
    page = LoginPage()
    page.openurl('http://127.0.0.1:8000')
    page.login(username,password)
    expect(page.check("Câu hỏi đã được tạo!"))



