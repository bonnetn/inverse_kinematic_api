FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk update && apk --no-cache add musl-dev linux-headers g++ && pip install pipenv


WORKDIR /app
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
RUN pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt

COPY ./main.py /app/main.py
