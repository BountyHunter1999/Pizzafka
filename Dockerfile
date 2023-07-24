FROM python:3.11.2-slim-bullseye AS builder

RUN apt-get update && apt-get upgrade --yes

RUN useradd --create-home pkafka
USER pkafka
WORKDIR /home/pkafka

ENV VIRTUALENV=/home/pkafka/venv
RUN python -m venv ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:${PATH}"

COPY pizza_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pizza_service/ /home/pkafka/pizza_service/
CMD ["flask", "--app", "pizza_service.app:app", "run", "--host", "0.0.0.0", "--port", "5000"]
