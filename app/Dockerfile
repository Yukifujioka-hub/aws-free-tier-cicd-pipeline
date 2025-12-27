FROM python:3.11-slim

WORKDIR /app

# Copy dependencies first (Docker cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app itself
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]