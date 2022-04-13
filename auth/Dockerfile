FROM snakepacker/python:all as builder

RUN python3.10 -m venv venv
COPY requirements.txt .
RUN venv/bin/pip install -U pip -r requirements.txt

FROM snakepacker/python:3.10 as tg-analytic-auth
COPY --from=builder venv venv

COPY /app/ .
