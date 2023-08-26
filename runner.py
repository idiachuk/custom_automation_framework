import subprocess

s = subprocess.run(f'python -m pytest -s -v --alluredir=allure_report tests/', shell=True, check=False)
s = subprocess.run(f'allure serve allure_report --port 8080', shell=True, check=False)
