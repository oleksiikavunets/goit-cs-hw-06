FROM python:3.11

RUN apt update

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "/app/main.py"]