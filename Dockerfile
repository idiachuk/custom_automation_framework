FROM mcr.microsoft.com/playwright/python:v1.36.0-focal

WORKDIR /usr/src/app

COPY ./ ./
USER root
RUN ls -ll
RUN python -m pip install --no-cache-dir -r requirements.txt
# Install Allure manually using wget and apt-get
RUN apt-get update && apt-get install -y wget default-jre
RUN wget -O allure-2.14.0.tgz https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.14.0/allure-commandline-2.14.0.tgz
RUN tar -zxvf allure-2.14.0.tgz -C /opt/
RUN ln -s /opt/allure-2.14.0/bin/allure /usr/bin/allure
RUN allure --version

EXPOSE 8080

ENTRYPOINT ["python",  "./runner.py"]