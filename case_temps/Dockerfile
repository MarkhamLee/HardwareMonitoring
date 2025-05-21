FROM python:3.13-3 AS builder

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc python3-dev libgpiod2

COPY case_temps/requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.13-3slim

RUN apt-get update -y && apt-get install -y libgpiod2

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY ./common ./common

WORKDIR /case_temps

COPY ./case_temps ./

ENTRYPOINT ["python3", "/case_temps/main.py"] 