FROM python:3.11.13-slim
# Устанавливаем рабочую директорию
WORKDIR /root/


COPY requirements.txt .
RUN apt-get update

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        firefox-esr \
        wget \
        xvfb \
        libdbus-glib-1-2 \
        libgtk-3-0 \
        && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz" && \
    tar -xzf geckodriver-*.tar.gz -C /usr/local/bin/ && \
    rm geckodriver-*.tar.gz && \
    chmod +x /usr/local/bin/geckodriver

ENV FIREFOX_BIN=/usr/bin/firefox-esr
ENV GECKODRIVER_PATH=/usr/local/bin/geckodriver
ENV MOZ_HEADLESS=1
ENV DISPLAY=:99

RUN mkdir -p /tmp/firefox-profile && \
    chmod -R 777 /tmp


RUN pip install --no-cache-dir -r requirements.txt

RUN pip install webdriver-manager
RUN pip install pytest-xdist

COPY . /root/
COPY entrypoint.sh /app/

ENTRYPOINT ["/app/entrypoint.sh"]
