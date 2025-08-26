FROM python:3.11.13-slim

COPY . /app/

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY entrypoint.sh /app/
WORKDIR /app/

ENTRYPOINT ["/app/entrypoint.sh"]
