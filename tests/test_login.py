from pages.login_page import LoginPage
from pages.question_page import QuestionPage
import pytest
import random
from playwright.sync_api import Page, expect

num = random.randint(0, 9999)
username = f'account{num}'
password = 'password'
def test_login(page:Page):
    login_page = LoginPage(page)
    login_page.openurl(f'file://{os.getcwd()}/index.html')
    login_page.login(username,password)
    expect(login_page.check("#question-section")).to_be_visible()



