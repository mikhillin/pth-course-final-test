import pytest
from playwright.sync_api import Page

from pages import HostingPage


@pytest.fixture(scope='function')
def hosting_page(page: Page) -> HostingPage:
    page.set_default_timeout(30000)
    hosting = HostingPage(page)
    hosting.open()
    hosting.wait()
    return hosting
