from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from tqdm import tqdm

from src.utils import datetime_Utils

from .dataset import Dataset
from .report_manager import ReportManager, SearchTrainingResult
    
class SearchPipeline:
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
        models: dict[str, Any],
        param_grids: dict[str, dict],
        report_path: str | Path,
        scorings: str | list[str],
        cv: int = 5,
        n_jobs: int = -1,
    ) -> None:

        self.dataset = dataset
        self.models: dict[str, Any] = models
        self.param_grids: dict[str, dict] = param_grids
        if isinstance(scorings, str):
            self.scorings = [scorings]
        else:
            self.scorings = scorings
        self.cv = cv
        self.n_jobs = n_jobs
        
        self.report_manager = ReportManager(report_path)
        
        
    def train_with_gridsearch(self) -> list[SearchTrainingResult]:

        results: list[SearchTrainingResult] = []

        for model_name, model in tqdm(
            self.models.items(),
            desc=f"Models ({self.models})",
            leave=False,
        ):
            for scoring in tqdm(
                self.scorings,
                desc=f"Scoring ({self.scorings})",
                leave=False,
            ):

                grid = self.param_grids.get(model_name, {})

                search = GridSearchCV(
                    estimator=model,
                    param_grid=grid,
                    scoring=scoring,
                    cv=self.cv,
                    n_jobs=self.n_jobs,
                    verbose=1
                )

                print("Début du train")
                search.fit(self.dataset.x_train, self.dataset.y_train)
                print("Fin du train")
                
                y_pred = search.best_estimator_.predict(self.dataset.x_test)
                
                metrics = ReportManager.compute_metrics(self.dataset.y_test, y_pred)
                matrix = confusion_matrix(
                            self.dataset.y_test,
                            y_pred,
                        ) 
                
                results.append(
                    SearchTrainingResult(
                        dataset_name=self.dataset.name,
                        model_name=model_name,
                        best_params=search.best_params_,
                        best_score=search.best_score_,
                        metrics=metrics,
                        matrix=matrix,
                        best_estimator=search.best_estimator_,
                        scoring=scoring
                    )
                )

        return results


    def run(self) -> None:
        """
        Exécute le pipeline complet.

        Étapes :
        1. Entraînement des modèles
        2. Génération du rapport CSV
        3. Sauvegarde des meilleurs modèles
        """

        results = self.train_with_gridsearch()
        now = datetime_Utils.DateTimeUtils.now('timestamp')
        print("Début du report")
        self.report_manager.generate_metrics(results, np.unique(self.dataset.y_test).tolist(), now)
        print("Fin du report")