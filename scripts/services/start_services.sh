#!/usr/bin/env bash

# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

set -e

NETWORK="hephaistos-dev"

# ==============================================================================
# Docker
# ==============================================================================

if ! docker info >/dev/null 2>&1; then

    echo "Démarrage de Docker..."

    if command -v systemctl >/dev/null 2>&1; then
        sudo systemctl start docker
    else
        echo "ERREUR : impossible de démarrer automatiquement Docker."
        exit 1
    fi

    until docker info >/dev/null 2>&1; do
        sleep 2
    done
fi

# ==============================================================================
# Network
# ==============================================================================

if ! docker network inspect "$NETWORK" >/dev/null 2>&1; then
    echo "Création du réseau Docker $NETWORK..."
    docker network create "$NETWORK"
fi

# ==============================================================================
# MLflow
# ==============================================================================

if docker inspect mlflow >/dev/null 2>&1; then

    echo "Démarrage de MLflow..."
    docker start mlflow

else

    echo "Création de MLflow..."

    docker run -d \
        --name mlflow \
        --network "$NETWORK" \
        -p 5000:5000 \
        -v "$(pwd)/mlflow:/mlflow" \
        ghcr.io/mlflow/mlflow:v3.10.1 \
        mlflow server \
        --host 0.0.0.0 \
        --port 5000 \
        --allowed-hosts "localhost:*,127.0.0.1:*,mlflow:5000" \
        --backend-store-uri sqlite:////mlflow/mlflow.db \
        --artifacts-destination /mlflow/artifacts
fi

# ==============================================================================
# Elasticsearch
# ==============================================================================

if docker inspect elasticsearch >/dev/null 2>&1; then

    echo "Démarrage de Elasticsearch..."
    docker start elasticsearch

else

    echo "Création de Elasticsearch..."

    docker run -d \
        --name elasticsearch \
        --network "$NETWORK" \
        -p 9200:9200 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
        -v elasticsearch_data:/usr/share/elasticsearch/data \
        docker.elastic.co/elasticsearch/elasticsearch:9.3.0
fi

# ==============================================================================
# Kibana
# ==============================================================================

if docker inspect kibana >/dev/null 2>&1; then

    echo "Démarrage de Kibana..."
    docker start kibana

else

    echo "Création de Kibana..."

    docker run -d \
        --name kibana \
        --network "$NETWORK" \
        -p 5601:5601 \
        -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
        docker.elastic.co/kibana/kibana:9.3.0
fi

echo
echo "Services démarrés :"
echo "MLflow        : http://localhost:5000"
echo "Elasticsearch : http://localhost:9200"
echo "Kibana        : http://localhost:5601"