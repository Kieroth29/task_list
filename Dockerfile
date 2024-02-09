FROM python:3.11.2-buster

WORKDIR /api

RUN apt update
RUN apt install gcc musl-dev

COPY ./backend/requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt

COPY ./backend .

CMD ["python", "main.py"]