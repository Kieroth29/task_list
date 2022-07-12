FROM python:3.8.10-buster
WORKDIR /api
RUN apt install gcc musl-dev linux-headers
COPY ./backend/requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
COPY ./backend .
CMD ["python main.py"]