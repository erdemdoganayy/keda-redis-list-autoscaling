# Python tabanlı bir resmi imaj kullanın
FROM python:3.9

COPY ./app /app

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "redis-client-simulator.py"]
