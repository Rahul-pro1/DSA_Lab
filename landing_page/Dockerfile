FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8507

CMD ["streamlit", "run", "app.py", "--server.port=8507", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
