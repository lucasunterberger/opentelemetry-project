FROM python:3.12-alpine

# Set up environment varibles for Python that make sense for a container
ENV PYTHONDONTWRITEGYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set env var for OTel
# ENV OTEL_SERVICE_NAME="flask-otel-test"
# ENV OTEL_TRACES_EXPORTER=console,otlp
# ENV OTEL_METRICS_EXPORTER=console
# ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=0.0.0.0:4317

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# to get OTel to run on alpine
# RUN apk add python3-dev
# RUN apk add build-base

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# bootstrap opentelemetry
RUN opentelemetry-bootstrap -a install

# Copy the entire application code
COPY . .

# Expose the port your application will run on
EXPOSE 8080

# Specify the command to run on container start
CMD ["python3", "src/app.py"]