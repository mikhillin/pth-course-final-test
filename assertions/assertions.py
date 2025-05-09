import allure


@allure.step('Asserting all prices have currency symbol: {symbol}')
def assert_prices_have_symbol(prices: list[str] ,symbol: str) -> None:
    symbols = {'EUR': '€', 'USD': '$'}
    
    assert symbol in symbols, f'Invalid currency. Should be in {symbols.keys()}'
    assert all(symbols[symbol] in price for price in prices), \
        f'Prices are not filtered by {symbol}'