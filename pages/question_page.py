from pages.base_page import BasePage


class QuestionPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.question = page.get_by_role("textbox", name="Câu hỏi")
        self.answer = page.get_by_role("textbox", name="Câu trả lời")
        self.submit = page.get_by_role("button", name="Gửi câu hỏi")
    def submit_question(self,question,answer):
        self.question.fill(question)
        self.answer.fill(answer)
        self.submit.click()
