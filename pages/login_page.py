from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="Đăng nhập")
    def login(self,username,password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_btn.click()
