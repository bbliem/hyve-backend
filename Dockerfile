FROM python:3.9-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Workaround for an error about trying to build the wheel for the cryptography package; see https://github.com/docker/compose/issues/8105
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN mkdir -p /wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/requirements.txt


FROM python:3.9-alpine

ENV APP_HOME=/home/app

RUN apk update && apk add libpq jpeg ffmpeg
COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir /wheels/*
# Workaround for an issue described here: https://stackoverflow.com/questions/65122957/resolving-new-pip-backtracking-runtime-issue
RUN pip install --use-deprecated=legacy-resolver --no-cache-dir /wheels/*
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
COPY . $APP_HOME

RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME
USER app
WORKDIR $APP_HOME
