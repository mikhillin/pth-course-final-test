from playwright.sync_api import Page, Locator

from .base_page import BasePage


class HostingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, '/hosting')
        self.currency_toggle = page.locator('gcore-switcher-currency')
        
    def select_server_type(self, type: str) -> Locator:
        type_toggle = self.page.locator('gcore-switch-buttons')
        label = type_toggle.locator(f'label:has-text("{type}")')
        label.click()
        value = 'vps' if type == 'Virtual servers' else 'dedicated'
        return label.locator(f'input[value={value}]')
    
    def get_currency(self) -> str | None:
        return self.currency_toggle.locator('input[type="radio"]:checked').get_attribute("value")
    
    def switch_currency(self) -> str | None:
        self.currency_toggle.click()
        return self.get_currency()

    def get_prices(self, all: bool = False) -> list[str]:
        while all:
            button = self.page.locator("button:has-text('Show more')")
            if not button.is_visible():
                break
            button.click()
            
        return self.page.locator('.gc-price-card-header .gc-text_36').all_inner_texts()
    
    def set_prices(self, min: str, max: str) -> None:
        price_filter = self.page.locator('gcore-price-filter')
        price_filter.click()
        
        def set_price(value: str, is_max: bool = True) -> Locator:
            index = 1 if is_max else 0
            elem = price_filter.locator('input[type="number"]').nth(index)
            elem.evaluate("(el, val) => el.value = val", value)
            return elem
            
        min_input = set_price(min, is_max = False)
        max_input = set_price(max, is_max = True)
        
        for input_elem in [min_input, max_input]:
            input_elem.dispatch_event("input")

 
        
