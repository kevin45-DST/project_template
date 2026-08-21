# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.logs.log_storage.log_storage_backend import LogStorageBackend


class LokiBackend(LogStorageBackend):
    """
    Backend de stockage des logs dans Grafana Loki.

    Les logs sont envoyés à Loki via son API HTTP.
    Le backend ne réalise aucun filtrage des logs.
    """

    def __init__(
        self,
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Initialise le backend Loki.

        Args:
            url: URL de l'API push de Loki.
            labels: Labels statiques associés aux logs.
        """
        project_config = ConfigManager("config/project.yaml")
        
        self._url = project_config.get("logs.storage.url")
        
        self._push_url = f"{self._url}/loki/api/v1/push"
        self._labels = labels or {}

    def store(self, log: dict[str, Any]) -> None:
        """
        Envoie un log à Loki.

        Args:
            log: Log à stocker.
        """

        timestamp = self._get_timestamp(log)
        payload = self._build_payload(log, timestamp)

        request = Request(
            self._push_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request) as response:
            response.read()

    def close(self) -> None:
        """Ferme le backend Loki."""

    def _build_payload(
        self,
        log: dict[str, Any],
        timestamp: int,
    ) -> dict[str, Any]:
        """Construit le payload attendu par l'API Loki."""

        labels = {
            **self._labels,
            "level": str(log.get("level", "UNKNOWN")).lower(),
            "logger": str(log.get("logger", "unknown")),
        }

        return {
            "streams": [
                {
                    "stream": labels,
                    "values": [
                        [
                            str(timestamp),
                            json.dumps(
                                log,
                                ensure_ascii=False,
                            ),
                        ]
                    ],
                }
            ]
        }

    @staticmethod
    def _get_timestamp(log: dict[str, Any]) -> int:
        """
        Convertit le timestamp du log en nanosecondes UTC.

        Args:
            log: Log contenant le timestamp ISO 8601.

        Returns:
            Timestamp Unix exprimé en nanosecondes.
        """
        timestamp = log.get("timestamp")

        if not timestamp:
            return int(datetime.now().timestamp() * 1_000_000_000)

        parsed_timestamp = datetime.fromisoformat(timestamp)

        return int(parsed_timestamp.timestamp() * 1_000_000_000)