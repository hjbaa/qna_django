# pull official base image
FROM python:3.10.10-alpine

# set work directory
WORKDIR /askme

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
# copy project

# run entrypoint.sh
ENTRYPOINT ["/askme/entrypoint.sh"]
