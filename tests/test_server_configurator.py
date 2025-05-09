import pytest
import allure
from playwright.sync_api import expect
import assertions


@allure.title('Checking the server type switch')
@allure.description('''
Test checks:
- general functionality of the server type toggle
- addaptive of filter set when changing the server type
- addaptive of server cards when changing the server type
''')
def test_server_type_switcher(hosting_page):    
    filter_options = { 
        "Dedicated servers": ["Data center", "CPU", "RAM", "Disk", "RAID", "GPU", "Price", "1 month"],
        "Virtual servers": ["Data center", "CPU", "RAM", "Disk", "Type", "OS", "Price"],
        }
    
    for server_type, expected_filters in filter_options.items():
        current_cards = hosting_page.get_prices()
        
        selected_type = hosting_page.select_server_type(server_type)
        expect(selected_type).to_be_checked()
        
        selected_filters = hosting_page.get_filters()
        assert selected_filters == expected_filters, f'Filter set did not change when selecting {server_type}'
        
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
    original = hosting_page.get_currency()
    prices = hosting_page.get_prices()
    assertions.assert_prices_have_symbol(prices, symbol=original)
    
    switched = hosting_page.switch_currency()
    prices = hosting_page.get_prices()
    assert switched != original, f'Currency has not switched from {original} to {switched}'
    assertions.assert_prices_have_symbol(prices, symbol=switched)
    
    returned = hosting_page.switch_currency()
    prices = hosting_page.get_prices()
    assert returned == original, f'Currency has not switched back from {switched} to {original}'
    assertions.assert_prices_have_symbol(prices, symbol=returned)

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
    assert min_price >= min_value and max_price <= max_value, \
        'Servers are shown outside of the price filter'