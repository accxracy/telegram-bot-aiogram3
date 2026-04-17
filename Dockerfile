FROM python:3.12-slim as build

WORKDIR /app


RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

RUN groupadd -r aiogram && useradd -r -g aiogram aiogram

WORKDIR /app

COPY --from=build --chown=aiogram:aiogram /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=aiogram:aiogram . .

USER aiogram

CMD ["python", "main.py"]



