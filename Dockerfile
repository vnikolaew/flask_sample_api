FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y openssl \

LABEL authors="Victorio Nikolaev"

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN chmod +x /app/certs/gen-certs.sh
RUN pip install -r requirements.txt

CMD ["/app/certs/gen-certs.sh"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--cert=./certs/cert.pem", "--key=./certs/key.pem"]