FROM python:3.10-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements-app.txt .
RUN pip install -r requirements-app.txt

# copy project
COPY . .

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 9999

