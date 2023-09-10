FROM python:3.7-slim-buster

RUN pip install pip==20.2.4

COPY app.py requirements.txt /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]