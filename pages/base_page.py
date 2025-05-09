from playwright.sync_api import Page


class BasePage:
    BASE_URL = 'https://gcore.com'

    def __init__(self, page: Page, path: str) -> None:
        self.page = page
        self.path = path
        self.url = f'{self.BASE_URL}{self.path}'

    def open(self, timeout: int = 2000) -> None:
        self.page.goto(self.url)

    def wait(self, timeout: int = 5000) -> None:
        self.page.wait_for_timeout(timeout)
