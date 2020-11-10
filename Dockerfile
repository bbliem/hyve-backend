FROM python:3.8-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt /tmp
COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /tmp/requirements.txt

FROM python:3.8-alpine

RUN apk update && apk add libpq
COPY --from=builder /app/wheels /wheels
COPY --from=builder /tmp/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/static
WORKDIR $APP_HOME
COPY . $APP_HOME

RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME
USER app
