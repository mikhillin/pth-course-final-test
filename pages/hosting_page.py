import allure
from playwright.sync_api import expect, Page, Locator

from .base_page import BasePage
from .locators import HostingPageLocators as HPL


class HostingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, '/hosting')
        self.currency_toggle = page.locator(HPL.CURRENCY_TOGGLE)

    @allure.step('Selecting a {server_type}')
    def select_server_type(self, server_type: str) -> Locator:
        type_toggle = self.page.locator(HPL.SERVER_TYPE_TOGGLE)
        label = type_toggle.locator(HPL.label_by_type(server_type))
        expect(label).to_be_visible()
        label.click()
        self.wait()
        value = 'vps' if server_type == 'Virtual servers' else 'dedicated'
        return label.locator(HPL.input_by_value(value))

    @allure.step('Getting current currency')
    def get_currency(self) -> str | None:
        return self.currency_toggle.locator(HPL.CHECKED_CURRENCY).get_attribute('value')

    @allure.step('Changing currency')
    def switch_currency(self) -> str | None:
        expect(self.currency_toggle).to_be_visible()
        self.currency_toggle.click()
        return self.get_currency()

    @allure.step('Getting list of the servers; all = {show_all}')
    def get_prices(self, show_all: bool = False) -> list[str]:
        while show_all:
            button = self.page.locator(HPL.SHOW_MORE_BTN)
            if not button.is_visible():
                break
            expect(button).to_be_visible()
            button.click()

        return self.page.locator(HPL.PRICE_CARDS).all_inner_texts()

    @allure.step('Setting the {value} price to the filter')
    def _set_price_input(self, price_filter: Locator, value: str, is_max: bool) -> None:
        index = 1 if is_max else 0
        elem = price_filter.locator(HPL.PRICE_INPUT_FIELDS).nth(index)
        elem.evaluate('(el, val) => el.value = val', value)
        elem.dispatch_event('input')

    @allure.step('Setting the price filter from {min} to {max}')
    def set_prices(self, min: str, max: str) -> None:
        price_filter = self.page.locator(HPL.PRICE_FILTER)
        expect(price_filter).to_be_visible()
        price_filter.click()

        self._set_price_input(price_filter, min, is_max=False)
        self._set_price_input(price_filter, max, is_max=True)

    @allure.step('Getting filters set')
    def get_filters(self) -> list[str]:
        return self.page.locator(HPL.FILTER_BAR).all_inner_texts()
