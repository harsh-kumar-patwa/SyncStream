FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the app has write permissions
RUN chmod -R 755 /app

CMD ["sh", "-c", "python main.py || (echo 'Application exited with an error. Keeping container alive for debugging.' && tail -f /dev/null)"]
