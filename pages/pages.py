from playwright.sync_api import Page, expect

class Login:
    def __init__(self, page):
        self.page = page

    @property
    def login_field(self):
        return self.page.get_by_placeholder("Username")

    @property
    def pasword_field(self):
        return self.page.get_by_placeholder("Password")

    @property
    def login_button(self):
        return self.page.locator('//input[@type="submit"]')

    def submit_login_form(self, user):
        self.login_field.fill(user["username"])
        self.pasword_field.fill(user["password"])
        self.login_button.click()

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")


class Inventory:
    def __init__(self, page):
        self.page = page

    @property
    def shopping_items(self):
        return self.page.locators('//div[@id="inventory_container"]')

    def shopping_item(self, name):
        return self.page.locator(f'//div[@class="inventory_item_name" and text() = "{name}"]/../../following-sibling::div/button')

    def add_item_to_cart(self, name):
        self.shopping_item(name).click()


class Cart:
    def __init__(self, page):
        self.page = page

    @property
    def cart_button(self):
        return self.page.locator('//a[@class="shopping_cart_link"]')

    @property
    def checkout_button(self):
        return self.page.get_by_role("button", name="Checkout")

    def shopping_item(self, name):
        return self.page.locator(
            f'//div[@class="inventory_item_name" and text() = "{name}"]/../following-sibling::div/button')

    def cart_button_click(self):
        self.cart_button.click()

    def remove_item_from_cart(self, product_name):
        self.shopping_item(product_name).click()

    def click_checkout(self):
        self.checkout_button.click()


class Checkout:
    def __init__(self, page):
        self.page = page

    @property
    def firstname_field(self):
        return self.page.get_by_placeholder("First Name")

    @property
    def lastname_field(self):
        return self.page.get_by_placeholder("Last Name")

    @property
    def zip_field(self):
        return self.page.get_by_placeholder("Zip/Postal Code")

    @property
    def continue_button(self):
        return self.page.locator('//input[@id="continue"]')

    @property
    def finish_button(self):
        return self.page.get_by_role("button", name="Finish")

    def order_confirmation_text(self):
        return self.page.get_by_role("heading", name="Thank you for your order!")

    def get_items_quantity(self):
        return self.page.locator('//div[@class="cart_quantity"]')

    def get_cart_quantity(self):
        return self.page.locator('//span[@class="shopping_cart_badge"]')

    def cart_items_names(self):
        elements = self.page.locator('//div[@class="inventory_item_name"]').all_text_contents()
        return elements

    def page_url(self):
        return self.page.url

    def complete_confirmation_text(self):
        return self.page.locator('//div[@class="complete-text"]')

    def checkout_complete_text(self):
        return self.page.locator('//span[@class="title"]')

    def back_home_button(self):
        return self.page.get_by_role("button", name="Back Home")

    def submit_checkout_form(self, checkout):
        self.firstname_field.fill(checkout["firstname"])
        self.lastname_field.fill(checkout["lastname"])
        self.zip_field.fill(checkout["zip"])
        self.continue_button.click()

    def expected_quantity_of_the_item(self, expected_num):
        expect(self.get_items_quantity()).to_have_text(str(expected_num))

    def expected_cart_quantity(self, expected_num):
        expect(self.get_cart_quantity()).to_have_text(str(expected_num))

    def verify_cart_contains_only(self, item_name):
        for i in self.cart_items_names():
            assert item_name == i

    def click_finish(self):
        self.finish_button.click()

    def validate_order_confirmed(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
        expect(self.order_confirmation_text()).to_be_visible()
        expect(self.complete_confirmation_text()).to_have_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!")
        expect(self.checkout_complete_text()).to_have_text("Checkout: Complete!")
        expect(self.back_home_button()).to_be_visible()
