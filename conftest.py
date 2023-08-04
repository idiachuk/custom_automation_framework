import pytest
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if 'browser' in item.fixturenames:
            try:
                from playwright.sync_api import Page
            except ImportError:
                return
        else:
            print('Fail to take screen-shot')
            return

        if "page" in item.fixturenames:
            page: Page = item.funcargs["page"]
            screenshot_bytes = page.screenshot()
            allure.attach(screenshot_bytes, name="Screenshot", attachment_type=allure.attachment_type.PNG)
