from pages.base_page import BasePage

class SignupPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="Đăng nhập")
        self.signup_btn = page.get_by_role("button", name="Đăng ký")
    def signup(self,username,password):
        self.username.click()
        self.username.fill(username)
        self.password.click()
        self.password.fill(password)
        self.login_btn.click()
    def login(self,username,password):
        self.username.click()
        self.username.fill(username)
        self.password.click()
        self.password.fill(password)
        self.login_btn.click()

