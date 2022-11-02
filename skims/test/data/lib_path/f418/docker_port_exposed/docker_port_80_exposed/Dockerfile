FROM node:16-alpine@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23 AS build

WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["flask", "run"]
USER node
