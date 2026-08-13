# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from __future__ import annotations

import time

import numpy as np

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.evaluation.evaluation_manager import EvaluationManager
from src.ml_toolbox.data_science.training.training_manager import TrainingManager

from src.ml_toolbox.transversal.persistence.model_persistence_manager import ModelPersistenceManager
from src.utils.ids_utils import runId

from ..ml_toolbox.data_science.data.dataset.dataset import Dataset
from ..ml_toolbox.transversal.reporting.report_manager import ReportManager, TrainingResult
    
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
    ) -> None:
        
        project_config = ConfigManager(
            "config/project.yaml"
        ) 
        
        self.dataset = dataset
        
        self.model_name = project_config.get("model.name")
        
        self.run_id = runId.create()

        self.training_manager = TrainingManager.create(
            model_name=self.model_name,
            dataset=self.dataset,
        )
        
        self.report_manager = ReportManager(run_id = self.run_id, mode="training")
        
        self.persistence_manager = ModelPersistenceManager.create()
        
        self.evaluation_manager = None
        
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

        # Top démarrage entrainement
        start_time = time.perf_counter()
        self.training_manager.train()
        # top fin d'entrainement
        end_time = time.perf_counter()
        # calcul de la durée d'entrainement
        training_duration = end_time - start_time
               
        self.evaluation_manager = EvaluationManager.create(self.training_manager.model, self.model_name, self.dataset)
        
        evaluation = self.evaluation_manager.evaluate()
        
        result = TrainingResult(self.model_name, evaluation["metrics"], evaluation["matrix"])
        
        self.report_manager.generate_metrics(result, np.unique(self.dataset.y_test).tolist(), training_duration)
        
        model_id = (f"{self.model_name}_{self.run_id}")
        
        self.persistence_manager.save(self.training_manager.model, model_id)