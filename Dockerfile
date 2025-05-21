FROM python:3.14-slim

RUN apt-get update && apt-get install gpg

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements

COPY ./app .

ENTRYPOINT ["uvicorn", "main:app"]
