# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

$containers = @(
    "mlflow",
    "elasticsearch",
    "kibana"
)

$network = "hephaistos-dev"

# ==============================================================================
# Containers
# ==============================================================================

foreach ($container in $containers) {

    docker inspect $container *> $null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Suppression du conteneur $container..."
        docker rm -f $container
    }
    else {
        Write-Host "Conteneur $container absent."
    }
}

# ==============================================================================
# Network
# ==============================================================================

docker network inspect $network *> $null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Suppression du réseau Docker $network..."
    docker network rm $network
}

Write-Host ""
Write-Host "Services de développement supprimés."