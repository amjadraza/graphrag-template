# Use the official Python image as the base image
FROM python:3.11.5-slim
# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy application code
COPY . .

# Install the project
RUN poetry install

# Install the project
RUN poetry shell
