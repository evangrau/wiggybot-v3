FROM python:3.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Prevent Python from writing .pyc files & disable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy app into the image
WORKDIR /app
COPY classes ./classes
COPY cogs ./cogs
COPY cmds ./cmds
COPY main.py utils.py settings.py pyproject.toml uv.lock .env ./

# Ensure `uv`-installed binaries are on PATH
ENV PATH=/app/bin:$PATH

# Sync dependencies
RUN uv sync --frozen

ENTRYPOINT [ "uv", "run", "main.py" ]
