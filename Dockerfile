# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

FROM python:3.11-slim

WORKDIR /app

ARG ENVIRONMENT=docker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "Environment=${ENVIRONMENT}" \
    && python deployment/config_resolver.py --environment "${ENVIRONMENT}"

CMD ["python", "main.py"]