# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Replace apt sources with Chinese mirror (Tsinghua University)
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # FFmpeg for video rendering
    ffmpeg \
    # LaTeX for mathematical typesetting
    texlive-full \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-science \
    # Additional build tools and libraries
    gcc \
    g++ \
    make \
    cmake \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    # Utilities
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with Chinese PyPI mirror
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/output

# Expose the port the app runs on
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command to run the HTTP API server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
