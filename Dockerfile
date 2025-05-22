FROM python:3.12-slim

WORKDIR /app

COPY ./utils /app/utils
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update
RUN apt-get install -y libmagic1 libmagic-dev

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "main:server", "--log-level", "critical", "--host", "0.0.0.0", "--port", "8080"]