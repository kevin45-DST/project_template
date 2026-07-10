from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.metrics import confusion_matrix

from src.utils import datetime_Utils

from ..ml_toolbox.dataset.dataset import Dataset
from .report_manager import ReportManager, TrainingResult
    
class TrainingPipeline:
    """
    Pipeline responsable de l'entraînement et de l'évaluation d'un modèle.

    Cette classe orchestre les différentes étapes nécessaires à la création
    d'un modèle candidat :

    1. Application des hyperparamètres au modèle fourni.
    2. Entraînement du modèle sur le dataset d'apprentissage.
    3. Évaluation du modèle sur le dataset de test.
    4. Génération d'un rapport contenant les métriques et la matrice de confusion.
    5. Sauvegarde du modèle entraîné au format joblib.

    Le pipeline ne gère pas directement :
    
    - la préparation des données ;
    - la recherche d'hyperparamètres ;
    - la sélection du meilleur modèle parmi plusieurs candidats ;
    - le suivi MLOps.

    Ces responsabilités sont laissées aux composants spécialisés du framework.

    Parameters
    ----------
    dataset : Dataset
        Dataset contenant les jeux de données d'entraînement et de test.

    model : Any
        Modèle compatible avec l'API scikit-learn (`fit`, `predict`, `set_params`).

    model_name : str
        Nom utilisé pour identifier le modèle dans les rapports et les artefacts.

    params : dict[str, Any]
        Paramètres d'entraînement appliqués au modèle avant le fit.

    report_path : str | Path
        Répertoire dans lequel les rapports d'évaluation seront générés.

    candidate_path : str | Path
        Répertoire de sauvegarde des modèles entraînés.

    Examples
    --------
    >>> pipeline = TrainingPipeline(
    ...     dataset=dataset,
    ...     model=RandomForestClassifier(),
    ...     model_name="random_forest",
    ...     params={"n_estimators": 100},
    ...     report_path="reports",
    ...     candidate_path="models/candidates",
    ... )
    ...
    >>> pipeline.run()
    """

    def __init__(
        self,
        dataset: Dataset,
        model: Any,
        model_name: str,
        params: dict[str, Any],
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

        """
        Entraîne le modèle et calcule ses résultats d'évaluation.

        Cette méthode applique les paramètres configurés au modèle,
        réalise l'entraînement sur le jeu de données d'apprentissage,
        puis évalue les performances sur le jeu de test.

        Les éléments retournés sont :

        - le nom du modèle ;
        - les métriques calculées ;
        - la matrice de confusion.

        Returns
        -------
        TrainingResult
            Objet contenant les résultats d'évaluation du modèle entraîné.
        """
        
        self.model.set_params(**self.params)
        self.model.fit(self.dataset.x_train, self.dataset.y_train)
                
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
        Exécute le cycle complet d'entraînement d'un modèle candidat.

        Étapes réalisées :

        1. Entraînement du modèle.
        2. Calcul des métriques et de la matrice de confusion.
        3. Génération du rapport d'évaluation.
        4. Sauvegarde du modèle entraîné au format joblib.

        Le modèle sauvegardé correspond à un candidat entraîné.
        La sélection finale parmi plusieurs modèles relève d'un composant
        supérieur (par exemple un futur Decision Helper).
        """

        result = self.train()
        now = datetime_Utils.DateTimeUtils.now('timestamp')
        self.report_manager.generate_metrics(result, np.unique(self.dataset.y_test).tolist(), now)
               
        file_name = (
            f"{self.model_name}_"
            f"{now}"
            ".joblib"
        )
        
        file_path = Path(self.candidate_path) / f"{file_name}"
        joblib.dump(self.model, file_path)