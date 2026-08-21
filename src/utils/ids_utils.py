# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class runId:
    """
    Générateur d'identifiants uniques pour les runs.

    Les identifiants générés utilisent un horodatage suffisamment précis
    pour distinguer les différentes exécutions du framework.

    Format
    ------
    run_YYYYMMDD_HHMMSSffffff
    """
    @staticmethod
    def create() -> str:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S%f"
        )
        """
        Génère un nouvel identifiant de run.

        Returns
        -------
        str
            Identifiant unique du run.
        """
        return f"run_{timestamp}"