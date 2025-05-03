FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV VERSADE_PORT=9373
ENV VERSADE_LOG_LEVEL=INFO
ENV VERSADE_CORS_ORIGINS=*

# Expose the port
EXPOSE 9373

# Run the server
CMD ["python", "-m", "versade"]
