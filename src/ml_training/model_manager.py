"""
model_manager.py

Responsable de la sauvegarde, du chargement et de la sélection des modèles
issus des entraînements.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import joblib

from .training_manager import TrainingResult


class ModelManager:
    """
    Gestionnaire des modèles entraînés.

    Cette classe est responsable de :
    - la sauvegarde des modèles entraînés
    - la sélection des meilleurs modèles
    - la persistance sur disque

    Elle ne gère PAS :
    - l'entraînement
    - les métriques
    - les datasets
    - les rapports

    Comment utiliser
    ----------------
    >>> manager = ModelManager("models/candidates")
    >>> manager.save_best(results, top_k=3)
    """

    def __init__(self, output_path: str | Path) -> None:
        """
        Initialise le gestionnaire de modèles.

        Parameters
        ----------
        output_path : str | Path
            Dossier de sauvegarde des modèles.
        """

        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def save_best(
        self,
        results: List[TrainingResult],
        top_k: int = 3,
    ) -> List[Path]:
        """
        Sauvegarde les meilleurs modèles.

        Parameters
        ----------
        results : List[TrainingResult]
            Résultats d'entraînement.

        top_k : int
            Nombre de meilleurs modèles à sauvegarder.

        Returns
        -------
        List[Path]
            Chemins des modèles sauvegardés.
        """

        sorted_results = sorted(
            results,
            key=lambda r: r.best_score,
            reverse=True,
        )

        best_results = sorted_results[:top_k]

        saved_paths: List[Path] = []

        for result in best_results:

            file_name = (
                f"{result.dataset_name}_"
                f"{result.model_name}_"
                f"{result.best_score:.4f}.joblib"
            )

            file_path = self.output_path / file_name

            joblib.dump(result.best_estimator, file_path)

            saved_paths.append(file_path)

        return saved_paths

    def save(self, model, name: str) -> Path:
        """
        Sauvegarde un modèle unique.

        Parameters
        ----------
        model : Any
            Modèle entraîné.

        name : str
            Nom du fichier.

        Returns
        -------
        Path
            Chemin du modèle sauvegardé.
        """

        file_path = self.output_path / f"{name}.joblib"
        joblib.dump(model, file_path)

        return file_path