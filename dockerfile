FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
RUN pip install -U pip -r requirements.txt && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY create_db.sql ./
COPY .env ./

ENTRYPOINT ["python3", "polling_bot.py"]