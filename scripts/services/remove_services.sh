#!/usr/bin/env bash

# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

set -e

CONTAINERS=(
    "mlflow"
    "elasticsearch"
    "kibana"
)

NETWORK="hephaistos-dev"

# ==============================================================================
# Containers
# ==============================================================================

for container in "${CONTAINERS[@]}"; do

    if docker inspect "$container" >/dev/null 2>&1; then
        echo "Suppression du conteneur $container..."
        docker rm -f "$container"
    else
        echo "Conteneur $container absent."
    fi

done

# ==============================================================================
# Network
# ==============================================================================

if docker network inspect "$NETWORK" >/dev/null 2>&1; then
    echo "Suppression du réseau Docker $NETWORK..."
    docker network rm "$NETWORK"
fi

echo
echo "Services de développement supprimés."