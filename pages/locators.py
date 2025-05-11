class HostingPageLocators:
    CURRENCY_TOGGLE = 'gcore-switcher-currency'
    CHECKED_CURRENCY = 'input[type="radio"]:checked'
    SERVER_TYPE_TOGGLE = 'gcore-switch-buttons'
    PRICE_FILTER = 'gcore-price-filter'
    PRICE_INPUT_FIELDS = 'input[type="number"]'
    SHOW_MORE_BTN = 'button:has-text("Show more")'
    FILTER_BAR = 'gcore-filter-bar li'
    PRICE_CARDS = '.gc-price-card-header .gc-text_36'
        
    @staticmethod
    def label_by_type(server_type: str) -> str:
        return f'label:has-text("{server_type}")'
    
    @staticmethod
    def input_by_value(value: str) -> str:
        return f'input[value={value}]'