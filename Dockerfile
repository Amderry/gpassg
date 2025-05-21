FROM python:3.13-slim

RUN apt-get update && apt-get install -y gpg

WORKDIR /app

RUN chown 1000:1000 /app 

USER gpassg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

ENTRYPOINT ["uvicorn"]

CMD ["main:app"]
