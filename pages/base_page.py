from playwright.sync_api import Page, expect
import random

num = random.randint(0, 9999)
class BasePage():
    def __init__(self,page:Page):
        self.page = page
    def openurl(self,url):
        self.page.goto(url)



        