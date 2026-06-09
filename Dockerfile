FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /usr/src/app

COPY ./ ./
USER root
RUN ls -ll
RUN python -m pip install --no-cache-dir -r requirements.txt
# Install Allure CLI
RUN apt-get update && apt-get install -y wget default-jre
RUN wget -O allure-2.32.0.tgz https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz
RUN tar -zxvf allure-2.32.0.tgz -C /opt/
RUN ln -s /opt/allure-2.32.0/bin/allure /usr/bin/allure
RUN allure --version

EXPOSE 8080

ENTRYPOINT ["python",  "./runner.py"]
