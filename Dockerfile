FROM python:3.12-slim-bookworm
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install -y --no-install-recommends git && apt install wget && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . .
WORKDIR /workspace/app
ENV UV_NO_DEV=1
RUN uv sync --locked
CMD ["sh"]
