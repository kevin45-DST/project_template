@echo off
REM Copyright © 2026 Kévin DELANOUE
REM License: see LICENSE

set NETWORK=hephaistos-dev

REM =============================================================================
REM Containers
REM =============================================================================

for %%C in (mlflow elasticsearch kibana) do (

    docker inspect %%C >nul 2>&1

    if not errorlevel 1 (
        echo Suppression du conteneur %%C...
        docker rm -f %%C
    ) else (
        echo Conteneur %%C absent.
    )
)

REM =============================================================================
REM Network
REM =============================================================================

docker network inspect %NETWORK% >nul 2>&1

if not errorlevel 1 (
    echo Suppression du reseau Docker %NETWORK%...
    docker network rm %NETWORK%
)

echo.
echo Services de developpement supprimes.