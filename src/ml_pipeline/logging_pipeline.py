# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from src.ml_toolbox.transversal.logs.log_storage.log_storage_manager import LogStorageManager


class LoggingPipeline:
    """Pipeline responsable de la collecte des logs."""

    def __init__(self):
        """
        Initialise le pipeline de logging.

        Args:
            log_collector: Collecteur de logs utilisé par le pipeline.
        """
        self.log_storage = LogStorageManager.create()

    def run(self) -> None:
        """Lance la collecte des logs."""
        self.log_storage.store()