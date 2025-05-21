FROM python:3.13-slim

RUN apt-get update && apt-get install -y gpg

WORKDIR /app

RUN useradd -ms /bin/bash gpassg && chown 1000:1000 /app 

COPY requirements.txt .

RUN pip install -r requirements.txt

USER gpassg

RUN mkdir $HOME/.gnupg

COPY ./app .

ENTRYPOINT ["uvicorn"]

CMD ["main:app"]
