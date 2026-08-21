@echo off
REM Copyright © 2026 Kévin DELANOUE
REM License: see LICENSE

set NETWORK=hephaistos-dev

REM =============================================================================
REM Docker
REM =============================================================================

docker info >nul 2>&1

if errorlevel 1 (

    if not exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        echo ERREUR : Docker Desktop est introuvable.
        exit /b 1
    )

    echo Demarrage de Docker Desktop...

    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

    :wait_docker
    timeout /t 2 /nobreak >nul

    docker info >nul 2>&1

    if errorlevel 1 goto wait_docker
)

REM =============================================================================
REM Network
REM =============================================================================

docker network inspect %NETWORK% >nul 2>&1

if errorlevel 1 (
    echo Creation du reseau Docker %NETWORK%...
    docker network create %NETWORK%
)

REM =============================================================================
REM MLflow
REM =============================================================================

docker inspect mlflow >nul 2>&1

if errorlevel 1 (

    echo Creation de MLflow...

    docker run -d ^
        --name mlflow ^
        --network %NETWORK% ^
        -p 5000:5000 ^
        -v "%CD%\mlflow:/mlflow" ^
        ghcr.io/mlflow/mlflow:v3.10.1 ^
        mlflow server ^
        --host 0.0.0.0 ^
        --port 5000 ^
        --allowed-hosts "localhost:*,127.0.0.1:*,mlflow:5000" ^
        --backend-store-uri sqlite:////mlflow/mlflow.db ^
        --artifacts-destination /mlflow/artifacts

) else (
    echo Demarrage de MLflow...
    docker start mlflow
)

REM =============================================================================
REM Elasticsearch
REM =============================================================================

docker inspect elasticsearch >nul 2>&1

if errorlevel 1 (

    echo Creation de Elasticsearch...

    docker run -d ^
        --name elasticsearch ^
        --network %NETWORK% ^
        -p 9200:9200 ^
        -e "discovery.type=single-node" ^
        -e "xpack.security.enabled=false" ^
        -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" ^
        -v elasticsearch_data:/usr/share/elasticsearch/data ^
        docker.elastic.co/elasticsearch/elasticsearch:9.3.0

) else (
    echo Demarrage de Elasticsearch...
    docker start elasticsearch
)

REM =============================================================================
REM Kibana
REM =============================================================================

docker inspect kibana >nul 2>&1

if errorlevel 1 (

    echo Creation de Kibana...

    docker run -d ^
        --name kibana ^
        --network %NETWORK% ^
        -p 5601:5601 ^
        -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" ^
        docker.elastic.co/kibana/kibana:9.3.0

) else (
    echo Demarrage de Kibana...
    docker start kibana
)

echo.
echo Services demarres :
echo MLflow        : http://localhost:5000
echo Elasticsearch : http://localhost:9200
echo Kibana        : http://localhost:5601