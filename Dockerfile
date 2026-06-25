# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY bot.py .

# CMD ["python", "bot.py"]


FROM python:3.13
WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update 
RUN git clone https://github.com/dmtana/unitibot
RUN pip install --no-cache-dir -r /app/unitibot/requirements.txt
RUN chmod +x /app/unitibot/script.sh
CMD bash ./unitibot/script.sh