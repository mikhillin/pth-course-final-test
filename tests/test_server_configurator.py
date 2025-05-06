import pytest
from playwright.sync_api import expect


def test_server_type_switcher(hosting_page):    
    for type in ["Dedicated servers", "Virtual servers"]:
        current_type = hosting_page.select_server_type(type)
        expect(current_type).to_be_checked()
        # проверить, что меняются карточки
        # проверить, что появляются доп фильтры
        # возможно, добавить функцию, которая будет хранить все фильтры как объекты

def test_currency_switcher(hosting_page):
    symbols = {'EUR': '€', 'USD': '$'}
    
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
    
    
# нужны ли скриншоты, если нужны, то когда
# прикрутить allure и шаги
# возможно, добавить другие маркеры (если придумаю зачем)
# запихать все это в докер
# написать README