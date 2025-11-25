# Python backend with uv package manager
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync

# Copy application code
COPY . .

# Run the application with uv
CMD ["uv", "run", "python3", "main.py"]
