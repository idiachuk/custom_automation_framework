import pytest
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # A test failing under xfail is reported as skipped with a `wasxfail` attribute.
    xfailed = report.skipped and hasattr(report, "wasxfail")
    if report.when != "call" or not (report.failed or xfailed):
        return

    # Non-UI tests (e.g. API) have no `page` fixture — nothing to screenshot.
    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        screenshot_bytes = page.screenshot()
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return
    allure.attach(screenshot_bytes, name="Screenshot", attachment_type=allure.attachment_type.PNG)
