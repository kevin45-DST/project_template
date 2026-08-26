from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from tqdm import tqdm

from src.utils import datetime_Utils

from ..ml_toolbox.dataset.dataset import Dataset
from .report_manager import ReportManager, SearchTrainingResult
    
class SearchPipeline:
    """
    Pipeline de recherche et comparaison de modèles.

    Cette classe orchestre l'exploration de plusieurs candidats modèles
    en utilisant une recherche d'hyperparamètres basée sur GridSearchCV.

    Pour chaque modèle fourni, le pipeline :

    1. Récupère la grille d'hyperparamètres associée.
    2. Lance une recherche avec validation croisée selon un ou plusieurs
       critères d'évaluation.
    3. Sélectionne le meilleur estimateur trouvé.
    4. Évalue ce modèle sur le jeu de test.
    5. Stocke les résultats de comparaison dans un objet SearchTrainingResult.

    Le pipeline est responsable de la phase de recherche et d'évaluation
    comparative. Il ne gère pas :

    - la préparation des données ;
    - l'entraînement final d'un modèle sélectionné ;
    - le déploiement ;
    - le suivi MLOps.

    La sélection finale d'un modèle parmi les résultats peut être réalisée
    par un composant dédié (Decision Helper displonible dans la toolbox).

    Parameters
    ----------
    dataset : Dataset
        Dataset contenant les données d'entraînement et de test.

    models : dict[str, Any]
        Dictionnaire associant un nom de modèle à une instance
        compatible avec l'API scikit-learn.

    param_grids : dict[str, dict]
        Dictionnaire contenant les grilles d'hyperparamètres associées
        à chaque modèle.

    report_path : str | Path
        Répertoire dans lequel les rapports de recherche seront générés.

    scorings : str | list[str]
        Critères d'évaluation utilisés par GridSearchCV.

    cv : int, optional
        Nombre de folds utilisés pour la validation croisée, par défaut 5.

    n_jobs : int, optional
        Nombre de jobs parallèles utilisés par GridSearchCV,
        par défaut -1.

    Examples
    --------
    >>> pipeline = SearchPipeline(
    ...     dataset=dataset,
    ...     models={
    ...         "random_forest": RandomForestClassifier()
    ...     },
    ...     param_grids={
    ...         "random_forest": {
    ...             "n_estimators": [100, 200]
    ...         }
    ...     },
    ...     report_path="reports",
    ...     scorings=["f1", "accuracy"],
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
        """
        Recherche les meilleurs paramètres pour chaque modèle configuré.

        Pour chaque combinaison modèle / métrique d'évaluation :

        1. Exécute une recherche GridSearchCV.
        2. Entraîne les différents candidats avec validation croisée.
        3. Récupère le meilleur estimateur obtenu.
        4. Évalue ce modèle sur le jeu de test.
        5. Retourne les résultats détaillés de comparaison.

        Returns
        -------
        list[SearchTrainingResult]
            Liste contenant les résultats de recherche pour chaque couple
            modèle / critère d'évaluation.
        """
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

                search.fit(self.dataset.x_train, self.dataset.y_train)
                
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
                        cv_score=search.best_score_,
                        metrics=metrics,
                        matrix=matrix,
                        best_estimator=search.best_estimator_,
                        scoring=scoring
                    )
                )

        return results


    def run(self) -> None:
        """
        Exécute le pipeline complet de recherche de modèles.

        Étapes réalisées :

        1. Recherche des meilleurs hyperparamètres avec GridSearchCV.
        2. Évaluation des meilleurs estimateurs sur le jeu de test.
        3. Génération du rapport de comparaison des résultats.

        Le pipeline produit uniquement des résultats de recherche.
        L'entraînement final d'un modèle retenu relève d'un pipeline
        d'entraînement dédié.
        """

        results = self.train_with_gridsearch()
        now = datetime_Utils.DateTimeUtils.now('timestamp')
        print("Début du report")
        self.report_manager.generate_metrics(results, np.unique(self.dataset.y_test).tolist(), now)
        print("Fin du report")