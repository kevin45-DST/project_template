from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.metrics import confusion_matrix

from src.utils import datetime_Utils

from .dataset import Dataset
from .report_manager import ReportManager, TrainingResult
    
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
        dataset: Dataset,
        model: Any,
        model_name: str,
        params: dict[str, str],
        report_path: str | Path,
        candidate_path: str | Path,
    ) -> None:

        self.dataset = dataset
        self.model = model
        self.model_name = model_name
        self.params = params
        self.candidate_path = candidate_path
        
        self.report_manager = ReportManager(report_path)
        
    def train(self) -> TrainingResult:

        print("Début du train")
        self.model.set_params(**self.params)
        self.model.fit(self.dataset.x_train, self.dataset.y_train)
        print("Fin du train")
                
        y_pred = self.model.predict(self.dataset.x_test)
                
        metrics = ReportManager.compute_metrics(self.dataset.y_test, y_pred)
        matrix = confusion_matrix(
                    self.dataset.y_test,
                    y_pred,
                ) 

        return TrainingResult(
                    model_name=self.model_name,
                    metrics=metrics,
                    matrix=matrix,
                )


    def run(self) -> None:
        """
        Exécute le pipeline complet.

        Étapes :
        1. Entraînement des modèles
        2. Génération du rapport CSV
        3. Sauvegarde des meilleurs modèles
        """

        result = self.train()
        now = datetime_Utils.DateTimeUtils.now('timestamp')
        print("Début du report")
        self.report_manager.generate_metrics(result, np.unique(self.dataset.y_test).tolist(), now)
        print("Fin du report")
               
        file_name = (
            f"{self.model_name}_"
            f"{now}"
            ".joblib"
        )
        
        file_path = Path(self.candidate_path) / f"{file_name}"
        joblib.dump(self.model, file_path)