from playwright.sync_api import Page, expect
import random

num = random.randint(0, 9999)
class BasePage():
    def __init__(self,page:Page):
        self.page = page
    def openurl(self,url):
        self.page.goto(url)
    def click_element(self,selector):
        self.page.locator(selector).click()
    def check(self):
        self.page.locator("#question-section").click()
        return self.page.get_by_role("button", name="Gửi câu hỏi")

        