FROM python:3.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the MariaDB Connector/C dev libraries and a C compiler
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \ 
        libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Prevent Python from writing .pyc files & disable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy app into the image
WORKDIR /app
COPY db ./db
COPY sql ./sql
COPY cogs ./cogs
COPY cmds ./cmds
COPY main.py settings.py pyproject.toml uv.lock ./

# Ensure `uv`-installed binaries are on PATH
ENV PATH=/app/bin:$PATH

# Sync dependencies
RUN uv sync --frozen

ENTRYPOINT [ "uv", "run", "main.py" ]
