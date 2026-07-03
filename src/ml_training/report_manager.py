from __future__ import annotations
from pathlib import Path
from typing import List
import pandas as pd
from .training_manager import TrainingResult


class ReportManager:
    """
    Générateur de rapports d'entraînement.

    Cette classe transforme les résultats d'entraînement en fichier CSV.

    Responsabilités
    ----------------
    - conversion des résultats en DataFrame
    - export CSV
    - structuration des performances

    Elle ne gère PAS :
    - l'entraînement
    - la sélection de modèles
    - la sauvegarde de modèles

    Comment utiliser
    ----------------
    >>> reporter = ReportManager("reports")
    >>> reporter.generate(results)
    """

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate(self, results: List[TrainingResult]) -> Path:
        """
        Génère un rapport CSV.

        Parameters
        ----------
        results : List[TrainingResult]

        Returns
        -------
        Path
            Chemin du fichier généré.
        """

        rows = []

        for r in results:
            rows.append(
                {
                    "dataset": r.dataset_name,
                    "model": r.model_name,
                    "best_score": r.best_score,
                    "accuracy": r.metrics["accuracy"],
                    "precision": r.metrics["precision"],
                    "recall": r.metrics["recall"],
                    "f1": r.metrics["f1"],
                    "best_params": r.best_params,
                }
            )

        df = pd.DataFrame(rows)

        file_path = self.output_path / "training_report.csv"
        df.to_csv(file_path, index=False)

        return file_path