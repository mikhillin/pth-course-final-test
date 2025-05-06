FROM mcr.microsoft.com/playwright/python:v1.52.0

WORKDIR /qaa

COPY . /qaa

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["pytest", "-v", "--alluredir=allure-results"]