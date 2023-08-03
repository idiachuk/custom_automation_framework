import time

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
    "zip": "3139"}


class TestPurchase:
    def test_purchase_positive(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        cart_page = Cart(page)
        checkout_page = Checkout(page)
        login_page.navigate()
        # Log in as a `standard user`
        login_page.submit_login_form(user)
        inventory_page.validate_login_successful()
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

    def test_sort_items_by_name(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        login_page.navigate()
        login_page.submit_login_form(user)
        inventory_page.validate_login_successful()
        # Sort products by name
        inventory_page.verify_active_sorting_option("Name (A to Z)")
        # Validate that the sorting is right
        inventory_page.verify_sorting_by_name_is_correct()

    def test_sort_items_by_price(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        login_page.navigate()
        login_page.submit_login_form(user)
        inventory_page.validate_login_successful()
        # Sort products by price
        inventory_page.select_sorting_option("lohi")
        inventory_page.verify_active_sorting_option("Price (low to high)")
        # Validate that the sorting is right
        inventory_page.verify_sorting_by_price_is_correct()
