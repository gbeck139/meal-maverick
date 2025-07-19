# Start from a minimal Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only what's needed
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and static/templates
COPY . .

# Expose Flask port
EXPOSE 5000

# Optional: define environment vars
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=docker

# Run Flask app
CMD ["flask", "run"]
