FROM python:3.12-slim as build

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim


RUN groupadd -r fastapi && useradd -r -g fastapi fastapi

WORKDIR /app

COPY --from=build --chown=fastapi:fastapi /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=fastapi:fastapi . .


USER fastapi

CMD ["uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "5000"]