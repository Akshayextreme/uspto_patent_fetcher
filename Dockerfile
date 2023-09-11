FROM python:3.7-slim-buster

# RUN \
#   apt-get update && \
#   apt-get install ca-certificates && \
#   apt-get clean

# COPY company-ca.crt /usr/local/share/ca-certificates/
# RUN update-ca-certificates

RUN pip install pip==20.2.4

COPY app.py requirements.txt /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]