FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git libglib2.0-0 libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/dmtana/unitibot.git /app/unitibot

WORKDIR /app/unitibot

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY script.sh /usr/local/bin/unitibot-start.sh
RUN chmod +x /usr/local/bin/unitibot-start.sh

EXPOSE 8501

CMD ["bash", "/usr/local/bin/unitibot-start.sh"]
