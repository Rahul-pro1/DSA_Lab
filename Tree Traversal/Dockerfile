FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8506

CMD ["streamlit", "run", "app.py", "--server.port=8506", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
