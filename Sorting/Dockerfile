FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8505

CMD ["streamlit", "run", "app.py", "--server.port=8505", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
