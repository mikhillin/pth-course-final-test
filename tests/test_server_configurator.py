import pytest
import allure
from playwright.sync_api import expect


@allure.title('Checking the server type switch')
@allure.description('''
Test checks:
- general functionality of the server type toggle
- addaptive of filter set when changing the server type
- addaptive of server cards when changing the server type
''')
def test_server_type_switcher(hosting_page):    
    for server_type in ["Dedicated servers", "Virtual servers"]:
        filters = ["Data center", "CPU", "RAM", "Disk", "Type", "OS", "Price"] if server_type == "Virtual servers" \
            else ["Data center", "CPU", "RAM", "Disk", "RAID", "GPU", "Price", "1 month"]

        current_cards = hosting_page.get_prices()
        
        selected_type = hosting_page.select_server_type(server_type)
        expect(selected_type).to_be_checked()
        
        selected_filters = hosting_page.get_filters()
        assert selected_filters == filters, f'Filter set did not change when selecting {server_type}'
        
        selected_cards = hosting_page.get_prices()
        assert sorted(selected_cards) != sorted(current_cards), \
            f'Cards did not change when selecting {server_type}'

@allure.title('Checking the currency switch')
@allure.description('''
Test checks:
- general functionality of the currency toggle (twice)
- addaptive of the currency on the server cards
''')
def test_currency_switcher(hosting_page):
    symbols = {'EUR': '€', 'USD': '$'}
    
    @allure.step('Checking that the price on the cards have changed currency to {currency}')
    def assertion_currency(currency: str):
        prices = hosting_page.get_prices()
        assert all(symbols[currency] in price for price in prices), \
            f"Prices are not filtered by {currency}"

    original = hosting_page.get_currency()
    assert original in symbols
    assertion_currency(original)
    
    switched = hosting_page.switch_currency()
    assert switched != original and switched in symbols
    assertion_currency(switched)
    
    returned = hosting_page.switch_currency()
    assert returned == original and returned in symbols
    assertion_currency(returned)

@allure.title('Checking the price filter')
@pytest.mark.parametrize('min_value, max_value', [
    pytest.param(0, 100),
    pytest.param(30, 35),
    pytest.param(71, 72)
]) 
def test_price_filter(hosting_page, min_value, max_value):
    hosting_page.set_prices(str(min_value), str(max_value))
    prices = hosting_page.get_prices(all=True)
    min_price = float(min(prices)[1:])
    max_price = float(max(prices)[1:])
    assert min_price >= min_value and max_price <= max_value