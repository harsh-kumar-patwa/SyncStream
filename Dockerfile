FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the application has write permissions
RUN chmod -R 755 /app

# Create a shell script to run our app
RUN echo '#!/bin/sh\n\
python main.py\n\
if [ $? -ne 0 ]; then\n\
    echo "Application exited with an error. Keeping container alive for debugging."\n\
    tail -f /dev/null\n\
fi' > /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]