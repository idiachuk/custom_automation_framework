import time
from playwright.sync_api import Page, expect

from pages.pages import *

user = {
    "username": "standard_user",
    "password": "secret_sauce"
}
shopping_item_1 = "Sauce Labs Bolt T-Shirt"
shopping_item_2 = "Sauce Labs Bike Light"
checkout_info = {
    "firstname": "Igor",
    "lastname": "Diachuk",
    "zip": "3139"
}

class TestPurchase:
    def test_purchase_positive(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        cart_page = Cart(page)
        checkout_page = Checkout(page)
        login_page.navigate()
        # Log in as a `standard user`
        login_page.submit_login_form(user)
        # Find an item by name, then add it to the cart
        inventory_page.add_item_to_cart(shopping_item_1)
        # Find a second item by name, and add it to the cart as well
        inventory_page.add_item_to_cart(shopping_item_2)
        # Go to the cart
        cart_page.cart_button_click()
        # Find an item by name, then remove it from the cart
        cart_page.remove_item_from_cart(shopping_item_1)
        # Finish the purchase
        cart_page.click_checkout()
        checkout_page.submit_checkout_form(checkout_info)
        # It only contains the items that you want to purchase
        checkout_page.verify_cart_contains_only(shopping_item_2)
        # The Item Total is right
        checkout_page.expected_quantity_of_the_item(1)
        checkout_page.expected_cart_quantity(1)
        # Finish the purchase
        checkout_page.click_finish()
        # Validate that the website confirms the order
        checkout_page.validate_order_confirmed()