# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.logs.log_storage.log_storage_backend import (
    LogStorageBackend,
)


class ElasticSearchBackend(LogStorageBackend):
    """
    Backend de stockage des logs dans Elasticsearch.

    Chaque log est enregistré comme un document JSON dans un index Elasticsearch.
    Le backend ne réalise aucun filtrage des logs.
    """

    def __init__(
        self,
        index: str = "hephaistos-logs",
    ) -> None:
        """
        Initialise le backend Elasticsearch.

        Args:
            index: Nom de l'index Elasticsearch utilisé pour stocker les logs.
        """
        project_config = ConfigManager("config/project.yaml")

        self._url = project_config.get("logs.storage.url")
        self._index = index

        self._index_url = f"{self._url}/{self._index}/_doc"

    def store(self, log: dict[str, Any]) -> None:
        """
        Enregistre un log dans Elasticsearch.

        Args:
            log: Log à stocker.
        """
        payload = self._build_payload(log)

        request = Request(
            self._index_url,
            data=json.dumps(
                payload,
                ensure_ascii=False,
            ).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            response.read()

    def close(self) -> None:
        """Ferme le backend Elasticsearch."""

    @staticmethod
    def _build_payload(
        log: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Construit le document Elasticsearch à partir d'un log.

        Args:
            log: Log à stocker.

        Returns:
            Document JSON compatible avec Elasticsearch.
        """
        timestamp = log.get("timestamp")

        if not timestamp:
            timestamp = datetime.now().astimezone().isoformat()

        return {
            **log,
            "timestamp": timestamp,
        }