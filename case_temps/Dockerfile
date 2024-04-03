FROM python:3.12.2-slim as builder

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc python3-dev libgpiod2

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.12.2-slim

RUN apt-get update -y && apt-get install -y libgpiod2

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY ./common ./common

WORKDIR /case_monitor

COPY ./case_temps ./

ENTRYPOINT ["python3", "/case_monitor/main.py"] 