FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
RUN pip install -U pip -r requirements.txt && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY .env ./
RUN python3 add_start_data.py

ENTRYPOINT ["python3", "polling_bot.py"]