# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any


class LogStorageBackend(ABC):
    """Interface abstraite pour le stockage des logs."""

    @abstractmethod
    def store(self, log: dict[str, Any]) -> None:
        """Stocke un log."""

        pass

    @abstractmethod
    def close(self) -> None:
        """Ferme les ressources utilisées par le backend."""

        pass