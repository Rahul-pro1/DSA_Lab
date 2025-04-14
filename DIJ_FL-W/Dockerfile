FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8504

CMD ["streamlit", "run", "app.py", "--server.port=8504", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
