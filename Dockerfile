FROM python:3.12-slim-bookworm

# Install curl to fetch uv installer
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

# Install uv (Python packaging tool)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy only project metadata first (better layer caching)
COPY pyproject.toml /app/pyproject.toml

# Create and populate virtual environment for api-v2-deps
RUN uv sync --no-dev --group api-v2-deps

# Now copy the rest of the source
COPY . /app

EXPOSE 80

# Run FastAPI app with Uvicorn from the created venv
ENTRYPOINT [".venv/bin/uvicorn", "main_v2:app", "--host", "0.0.0.0", "--port", "80"]