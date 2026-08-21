# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

$dockerDesktop = "C:\Program Files\Docker\Docker\Docker Desktop.exe"

$network = "hephaistos-dev"

$mlflowContainer = "mlflow"
$elasticsearchContainer = "elasticsearch"
$kibanaContainer = "kibana"

# ==============================================================================
# Docker
# ==============================================================================

docker info *> $null

if ($LASTEXITCODE -ne 0) {

    if (-not (Test-Path $dockerDesktop)) {
        Write-Error "Docker Desktop est introuvable."
        exit 1
    }

    Write-Host "Démarrage de Docker Desktop..."
    Start-Process $dockerDesktop

    do {
        Start-Sleep -Seconds 2
        docker info *> $null
    } while ($LASTEXITCODE -ne 0)
}

# ==============================================================================
# Network
# ==============================================================================

docker network inspect $network *> $null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Création du réseau Docker $network..."
    docker network create $network
}

# ==============================================================================
# MLflow
# ==============================================================================

docker inspect $mlflowContainer *> $null

if ($LASTEXITCODE -eq 0) {

    Write-Host "Démarrage du conteneur MLflow existant..."
    docker start $mlflowContainer

} else {

    Write-Host "Création du conteneur MLflow..."

    docker run -d `
        --name $mlflowContainer `
        --network $network `
        -p 5000:5000 `
        -v "${PWD}\mlflow:/mlflow" `
        ghcr.io/mlflow/mlflow:v3.10.1 `
        mlflow server `
        --host 0.0.0.0 `
        --port 5000 `
        --allowed-hosts "localhost:*,127.0.0.1:*,mlflow:5000" `
        --backend-store-uri sqlite:////mlflow/mlflow.db `
        --artifacts-destination /mlflow/artifacts
}

# ==============================================================================
# Elasticsearch
# ==============================================================================

docker inspect $elasticsearchContainer *> $null

if ($LASTEXITCODE -eq 0) {

    Write-Host "Démarrage du conteneur Elasticsearch existant..."
    docker start $elasticsearchContainer

} else {

    Write-Host "Création du conteneur Elasticsearch..."

    docker run -d `
        --name $elasticsearchContainer `
        --network $network `
        -p 9200:9200 `
        -e "discovery.type=single-node" `
        -e "xpack.security.enabled=false" `
        -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" `
        -v elasticsearch_data:/usr/share/elasticsearch/data `
        docker.elastic.co/elasticsearch/elasticsearch:9.3.0
}

# ==============================================================================
# Kibana
# ==============================================================================

docker inspect $kibanaContainer *> $null

if ($LASTEXITCODE -eq 0) {

    Write-Host "Démarrage du conteneur Kibana existant..."
    docker start $kibanaContainer

} else {

    Write-Host "Création du conteneur Kibana..."

    docker run -d `
        --name $kibanaContainer `
        --network $network `
        -p 5601:5601 `
        -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" `
        docker.elastic.co/kibana/kibana:9.3.0
}

Write-Host ""
Write-Host "Services démarrés :"
Write-Host "MLflow        : http://localhost:5000"
Write-Host "Elasticsearch : http://localhost:9200"
Write-Host "Kibana        : http://localhost:5601"