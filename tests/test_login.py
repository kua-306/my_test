from pages.login_page import SignupPage
from pages.question_page import QuestionPage
import os
import random
from playwright.sync_api import Page, expect
import re

num = random.randint(0, 9999)
username = f'account{num}'
password = 'password'
def test_signup(page:Page):
    login_page = SignupPage(page)
    login_page.openurl(f'file://{os.getcwd()}/index.html')
    login_page.signup(username,password)
    expect(login_page.check()).not_to_be_enabled()
    login_page.login(username,password)
    expect(login_page.check()).to_be_enabled





