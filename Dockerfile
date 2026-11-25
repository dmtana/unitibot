# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY bot.py .

# CMD ["python", "bot.py"]


FROM python:3.13
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# Update pip
RUN pip install --upgrade pip
# Clone repository
RUN git clone https://github.com/dmtana/unitibot.git /app/unitibot

# Install Python dependencies
RUN pip install --no-cache-dir \
    -r /app/unitibot/requirements.txt
# Set permissions
RUN chmod +x /app/unitibot/script.sh
EXPOSE 8501
CMD ["bash", "/app/unitibot/script.sh"]