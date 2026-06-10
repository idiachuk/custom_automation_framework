import pytest
from pages.pages import *

user = {
    "username": "locked_out_user",
    "password": "secret_sauce"
}


class TestLogin:
    @allure.title("Negative Login")
    @pytest.mark.xfail(
        reason="Negative Login",
        strict=True)
    def test_login_negative(self, page):
        login_page = Login(page)
        inventory_page = Inventory(page)
        login_page.navigate()
        # Log in as a `locked_out_user`
        login_page.submit_login_form(user)
        inventory_page.validate_login_successful()

