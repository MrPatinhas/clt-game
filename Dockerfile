FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install Python dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source, data, and assets
COPY app/ ./app/
COPY assets/ ./assets/
COPY data/ ./data/

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request, os; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8000') + '/health')" || exit 1

CMD ["python", "app/main.py"]
