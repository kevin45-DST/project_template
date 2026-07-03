"""
training_pipeline.py

Orchestrateur principal du framework ML.

Cette classe coordonne :
- les datasets
- l'entraînement
- la génération des rapports
- la sauvegarde des modèles

Elle ne contient aucune logique métier.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .dataset import Dataset
from .model_manager import ModelManager
from .report_manager import ReportManager
from .training_manager import TrainingManager


class TrainingPipeline:
    """
    Orchestrateur global du pipeline de Machine Learning.

    Cette classe est le point d'entrée principal du framework.

    Elle ne fait qu'orchestrer les composants spécialisés :

    1. TrainingManager → entraînement des modèles
    2. ReportManager → génération du CSV
    3. ModelManager → sauvegarde des meilleurs modèles

    Comment utiliser
    ----------------
    >>> pipeline = TrainingPipeline(
    ...     datasets=datasets,
    ...     models=models,
    ...     param_grids=param_grids,
    ...     report_path="reports",
    ...     candidate_path="models/candidates",
    ...     scoring="f1",
    ...     cv=5,
    ...     top_k=3,
    ... )
    ...
    >>> pipeline.run()
    """

    def __init__(
        self,
        datasets: list[Dataset],
        models: dict[str, Any],
        param_grids: dict[str, dict],
        report_path: str | Path,
        candidate_path: str | Path,
        scoring: str = "f1",
        cv: int = 5,
        top_k: int = 3,
    ) -> None:

        self.datasets = datasets
        self.top_k = top_k

        self.training_manager = TrainingManager(
            models=models,
            param_grids=param_grids,
            scoring=scoring,
            cv=cv,
        )

        self.report_manager = ReportManager(report_path)

        self.model_manager = ModelManager(candidate_path)

    def run(self) -> None:
        """
        Exécute le pipeline complet.

        Étapes :
        1. Entraînement des modèles
        2. Génération du rapport CSV
        3. Sauvegarde des meilleurs modèles
        """

        results = self.training_manager.train(self.datasets)

        self.report_manager.generate(results)

        self.model_manager.save_best(
            results=results,
            top_k=self.top_k,
        )