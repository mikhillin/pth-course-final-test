import pytest
from playwright.sync_api import Page
from pages import HostingPage


@pytest.fixture(scope='function')
def hosting_page(page: Page) -> HostingPage:
    hosting = HostingPage(page)
    hosting.open()
    hosting.wait()
    return hosting