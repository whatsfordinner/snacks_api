FROM python:3.8-alpine
WORKDIR /app
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN apk add --no-cache --virtual build-deps gcc musl-dev libressl-dev libffi-dev && \
pip install -r requirements.txt && \
pip install uwsgi
COPY ./snacks ./snacks
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--module", "snacks:create_app()"]