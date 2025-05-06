import allure
from playwright.sync_api import expect, Page, Locator

from .base_page import BasePage


class HostingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, '/hosting')
        self.currency_toggle = page.locator('gcore-switcher-currency')
    
    @allure.step('Selecting a {type}')    
    def select_server_type(self, type: str) -> Locator:
        type_toggle = self.page.locator('gcore-switch-buttons')
        label = type_toggle.locator(f'label:has-text("{type}")')
        expect(label).to_be_visible(timeout=10000)
        label.click()
        self.wait(timeout=1000)
        value = 'vps' if type == 'Virtual servers' else 'dedicated'
        return label.locator(f'input[value={value}]')
    
    @allure.step('Getting current currency')
    def get_currency(self) -> str | None:
        return self.currency_toggle.locator('input[type="radio"]:checked').get_attribute("value")
    
    @allure.step('Changing currency')
    def switch_currency(self) -> str | None:
        expect(self.currency_toggle).to_be_visible(timeout=10000)
        self.currency_toggle.click()
        return self.get_currency()

    @allure.step('Getting list of the servers; all = {all}')
    def get_prices(self, all: bool = False) -> list[str]:
        while all:
            button = self.page.locator("button:has-text('Show more')")
            if not button.is_visible():
                break
            expect(button).to_be_visible(timeout=10000)
            button.click()
            
        return self.page.locator('.gc-price-card-header .gc-text_36').all_inner_texts()
    
    @allure.step('Setting the price filter from {min} to {max}')
    def set_prices(self, min: str, max: str) -> None:
        price_filter = self.page.locator('gcore-price-filter')
        expect(price_filter).to_be_visible(timeout=10000)
        price_filter.click()
        
        @allure.step('Setting the {value} price to the filter')
        def set_price(value: str, is_max: bool = True) -> Locator:
            index = 1 if is_max else 0
            elem = price_filter.locator('input[type="number"]').nth(index)
            elem.evaluate("(el, val) => el.value = val", value)
            return elem
            
        min_input = set_price(min, is_max = False)
        max_input = set_price(max, is_max = True)
        
        for input_elem in [min_input, max_input]:
            input_elem.dispatch_event("input")

    @allure.step('Getting filters set')
    def get_filters(self) -> list[str]:
        filter_bar = self.page.locator('gcore-filter-bar')
        filters = filter_bar.locator('li').all_inner_texts()
        return filters
        
