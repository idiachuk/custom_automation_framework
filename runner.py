import subprocess

s = subprocess.run(f'python -m pytest -s -v --screenshot=only-on-failure --alluredir=allure_report tests', shell=True, check=False)
s = subprocess.run(f'allure serve allure_report --port 8080', shell=True, check=False)

# python -m pytest -s -v --headed --screenshot=only-on-failure --alluredir=allure_report tests/test_purchase_positive.py
