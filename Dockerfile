FROM python:3.9.7-slim-buster

RUN apt-get update && apt-get install make

WORKDIR /NFD

COPY . .

EXPOSE 5000

RUN pip install -r dev_requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
