import allure
from playwright.sync_api import expect, Page, Locator

from .base_page import BasePage


class HostingPage(BasePage):
    CURRENCY_TOGGLE = 'gcore-switcher-currency'
    SERVER_TYPE_TOGGLE = 'gcore-switch-buttons'
    PRICE_FILTER = 'gcore-price-filter'
    SHOW_MORE_BTN = 'button:has-text("Show more")'
    FILTER_BAR = 'gcore-filter-bar'
    PRICE_CARDS = '.gc-price-card-header .gc-text_36'

    def __init__(self, page: Page) -> None:
        super().__init__(page, '/hosting')
        self.currency_toggle = page.locator(self.CURRENCY_TOGGLE)

    @allure.step('Selecting a {type}')
    def select_server_type(self, type: str) -> Locator:
        type_toggle = self.page.locator(self.SERVER_TYPE_TOGGLE)
        label = type_toggle.locator(f'label:has-text("{type}")')
        expect(label).to_be_visible(timeout=10000)
        label.click()
        self.wait(timeout=2000)
        value = 'vps' if type == 'Virtual servers' else 'dedicated'
        return label.locator(f'input[value={value}]')

    @allure.step('Getting current currency')
    def get_currency(self) -> str | None:
        return self.currency_toggle.locator('input[type="radio"]:checked').get_attribute('value')

    @allure.step('Changing currency')
    def switch_currency(self) -> str | None:
        expect(self.currency_toggle).to_be_visible(timeout=10000)
        self.currency_toggle.click()
        return self.get_currency()

    @allure.step('Getting list of the servers; all = {show_all}')
    def get_prices(self, show_all: bool = False) -> list[str]:
        while show_all:
            button = self.page.locator(self.SHOW_MORE_BTN)
            if not button.is_visible():
                break
            expect(button).to_be_visible(timeout=10000)
            button.click()

        return self.page.locator(self.PRICE_CARDS).all_inner_texts()

    @allure.step('Setting the {value} price to the filter')
    def _set_price_input(self, price_filter: Locator, value: str, is_max: bool) -> None:
        index = 1 if is_max else 0
        elem = price_filter.locator('input[type="number"]').nth(index)
        elem.evaluate('(el, val) => el.value = val', value)
        elem.dispatch_event('input')

    @allure.step('Setting the price filter from {min} to {max}')
    def set_prices(self, min: str, max: str) -> None:
        price_filter = self.page.locator(self.PRICE_FILTER)
        expect(price_filter).to_be_visible(timeout=10000)
        price_filter.click()

        self._set_price_input(price_filter, min, is_max=False)
        self._set_price_input(price_filter, max, is_max=True)

    @allure.step('Getting filters set')
    def get_filters(self) -> list[str]:
        filter_bar = self.page.locator(self.FILTER_BAR)
        filters = filter_bar.locator('li').all_inner_texts()
        return filters
