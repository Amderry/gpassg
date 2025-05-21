FROM python:3.13-slim

RUN apt-get update && apt-get install -y gpg

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements

COPY ./app .

ENTRYPOINT ["uvicorn"]

CMD ["main:app"]
