# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from pathlib import Path

import pandas as pd


class MetricsLoader:

    """
    Chargeur des résultats d'expérimentation.

    Cette classe permet de récupérer les informations persistées par les
    composants de génération de rapports.

    Elle fournit notamment :

    - les métriques globales des modèles ;
    - les matrices de confusion associées aux expériences.

    Les données chargées sont destinées à être exploitées par les composants
    de visualisation du DecisionHelper.

    Cette classe ne réalise :

    - aucun calcul de performance ;
    - aucune comparaison de modèles ;
    - aucune interprétation des résultats.
    """
    
    def __init__(
        self,
        report_path: Path,
    ) -> None:

        self.report_path = report_path
        
    def list_runs(self) -> list[str]:
        """
        Retourne la liste des runs disponibles.

        Chaque sous-répertoire du répertoire de recherche correspond
        à un run.
        """

        return sorted(
            path.name
            for path in self.report_path.iterdir()
            if path.is_dir()
        )

    def load(self) -> pd.DataFrame:

        return pd.read_csv(
            self.report_path / "report.csv"
        )
        
    def load_confusion_matrix(
        self,
        run_id: str,
    ) -> dict:

        file_path = (
            self.report_path
            / "confusion_matrix"
            / f"{run_id}_confusion_matrix.json"
        )
        print(f"{run_id = }")
        with open(
            file_path,
            encoding="utf-8",
        ) as file:

            return json.load(file)