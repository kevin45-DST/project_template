from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from .dataset import Dataset
from tqdm import tqdm
from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
        )

@dataclass(slots=True)
class TrainingResult:
    """
    Résultat d'un entraînement de modèle.

    Attributes
    ----------
    dataset_name : str
    model_name : str
    best_params : dict
    best_score : float
    metrics : dict
    best_estimator : Any
    """

    dataset_name: str
    model_name: str
    best_params: dict
    best_score: float
    metrics: dict
    best_estimator: Any


class TrainingManager:
    """
    Gestionnaire des entraînements de modèles ML.

    Cette classe est responsable de :
    - l'exploration des hyperparamètres (GridSearchCV)
    - l'entraînement des modèles
    - le calcul des performances
    - la production des résultats structurés

    Elle ne gère PAS :
    - la sauvegarde des modèles
    - la génération de rapports
    - la gestion des datasets

    Comment utiliser
    ----------------
    >>> manager = TrainingManager(
    ...     models=models,
    ...     param_grids=param_grids,
    ...     scoring="f1",
    ...     cv=5,
    ... )
    ...
    >>> results = manager.train(datasets)
    """

    def __init__(
        self,
        models: dict[str, BaseEstimator],
        param_grids: dict[str, dict],
        scoring: str,
        cv: int = 5,
        n_jobs: int = -1,
    ) -> None:

        self.models = models
        self.param_grids = param_grids
        self.scoring = scoring
        self.cv = StratifiedKFold(
                    n_splits=cv,
                    shuffle=True,
                    random_state=42
                )
        self.n_jobs = n_jobs

    def train(self, datasets: list[Dataset]) -> list[TrainingResult]:

        results: list[TrainingResult] = []

        for dataset in tqdm(datasets, desc="Datasets"):

            for model_name, model in tqdm(
                self.models.items(),
                desc=f"Models ({dataset.name})",
                leave=False,
            ):

                grid = self.param_grids.get(model_name, {})

                search = GridSearchCV(
                    estimator=model,
                    param_grid=grid,
                    scoring=self.scoring,
                    cv=self.cv,
                    n_jobs=self.n_jobs,
                    verbose=1
                )

                search.fit(dataset.x_train, dataset.y_train)

                y_pred = search.predict(dataset.x_test)

                metrics = self._compute_metrics(
                    dataset.y_test,
                    y_pred,
                )

                results.append(
                    TrainingResult(
                        dataset_name=dataset.name,
                        model_name=model_name,
                        best_params=search.best_params_,
                        best_score=search.best_score_,
                        metrics=metrics,
                        best_estimator=search.best_estimator_,
                    )
                )

        return results

    def _compute_metrics(self, y_true, y_pred) -> dict:
        """
        Calcule les métriques principales.
        """
        
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
        }