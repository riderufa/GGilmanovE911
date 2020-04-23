FROM python:3.6-alpine




ADD . /
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install psycopg2-binary
COPY entry.sh ./
RUN chmod +x entry.sh