
# unitibot

Quick calculation solution with Telegram Bot and Web Interface.

## Implementation

### 1. Create a file with the bot TOKEN

```bash
mkdir -p data

echo "TOKEN = 'YOUR_BOT_TOKEN_HERE'" > ./data/BOT_TOKEN.py
```

### 2. Build Docker image

```bash
sudo docker compose build --no-cache
```

### 3. Start the containers

```bash
sudo docker compose up -d
```

The following services will be started:

- Telegram Bot
- Streamlit Web Interface (Bellara Scanner)

### 4. Access the Web Interface

Local access:

http://localhost:8501

Remote access via SSH tunnel:

```bash
ssh -N -L 8501:127.0.0.1:8501 USER@SERVER_IP
```

For direct external access, configure port forwarding
or an HTTPS reverse proxy.

### 5. Docker management

Check container status:

```bash
sudo docker compose ps
```

View logs:

```bash
sudo docker compose logs -f
```

Restart containers:

```bash
sudo docker compose restart
```

Stop containers:

```bash
sudo docker compose down
```

### 6. Update the application

```bash
sudo docker compose build --no-cache
sudo docker compose up -d
```

## Technologies

- Python 3.13
- Aiogram
- Streamlit
- OpenCV
- NumPy
- Docker & Docker Compose

