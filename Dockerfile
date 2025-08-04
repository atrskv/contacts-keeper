FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin:/usr/local/bin:${PATH}"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY . .

EXPOSE 8000

CMD ["uv", "run", "flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=8000"]
