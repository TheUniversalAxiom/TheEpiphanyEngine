# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 epiphany && \
    chown -R epiphany:epiphany /app

# Copy Python dependencies from builder
COPY --from=builder --chown=epiphany:epiphany /root/.local /home/epiphany/.local

# Copy application code
COPY --chown=epiphany:epiphany . .

# Set environment variables
ENV PATH=/home/epiphany/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Switch to non-root user
USER epiphany

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://localhost:8000/api/health', timeout=5).read()" || exit 1

# Default command - run the web API
CMD ["uvicorn", "web.api:app", "--host", "0.0.0.0", "--port", "8000"]
