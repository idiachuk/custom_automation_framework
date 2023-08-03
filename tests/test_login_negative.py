from pages.pages import *

user = {
    "username": "locked_out_user",
    "password": "secret_sauce"
}


class TestLogin:
    def test_login_negative(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        login_page.navigate()
        # Log in as a `locked_out_user`
        login_page.submit_login_form(user)
        inventory_page.validate_login_successful()

