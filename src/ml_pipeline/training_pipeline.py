# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from __future__ import annotations

import time

import numpy as np

from config.config_manager import ConfigManager
from src.ml_toolbox.transversal.logs.log_collector.log_collector_manager import LogCollectorManager
from src.ml_toolbox.transversal.evaluation.evaluation_manager import EvaluationManager
from src.ml_toolbox.data_science.training.training_manager import TrainingManager

from src.ml_toolbox.transversal.persistence.model_persistence_manager import ModelPersistenceManager
from src.utils.ids_utils import runId

from ..ml_toolbox.data_science.data.dataset.dataset import Dataset
from ..ml_toolbox.transversal.reporting.report_manager import ReportManager, TrainingResult
    
class TrainingPipeline:
    """
    Pipeline responsable de l'entraînement, de l'évaluation et de la
    persistance d'un modèle.

    Cette classe orchestre les étapes suivantes :

    1. création du gestionnaire d'entraînement à partir de la configuration ;
    2. entraînement du modèle ;
    3. évaluation sur le jeu de test ;
    4. génération du rapport associé au run ;
    5. sauvegarde du modèle entraîné.

    Le pipeline ne gère pas directement :

    - la préparation des données ;
    - la recherche d'hyperparamètres ;
    - la sélection d'un modèle parmi plusieurs candidats ;
    - le suivi MLOps.

    Ces responsabilités sont déléguées aux composants spécialisés du
    framework.

    Parameters
    ----------
    dataset : Dataset
        Dataset contenant les données d'entraînement et de test.
    """

    def __init__(
        self,
        dataset: Dataset,
    ) -> None:
        """
        Initialise un nouveau run d'entraînement.

        Parameters
        ----------
        dataset : Dataset
            Dataset utilisé pour entraîner et évaluer le modèle.
        """        
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
        
        self.logger = LogCollectorManager()
        
    def run(self) -> None:

        self.logger.info(message="Début du run", logger=self.__class__.__name__, run_id=self.run_id)
        
        # Top démarrage entrainement
        start_time = time.perf_counter()
        
        self.logger.info(
            message="Début du train", 
            logger=self.__class__.__name__, 
            run_id=self.run_id, 
            context={"model_name":self.model_name})
        
        self.training_manager.train()
        # top fin d'entrainement
        end_time = time.perf_counter()
        # calcul de la durée d'entrainement
        training_duration = end_time - start_time
        self.logger.info(
            message="Fin du train", 
            logger=self.__class__.__name__, 
            run_id=self.run_id, 
            context={"model_name":self.model_name, "training_duration":training_duration})
               
        self.logger.info(
            message="Début de l'évaluation", 
            logger=self.__class__.__name__, 
            run_id=self.run_id, 
            context={"model_name":self.model_name})
        
        self.evaluation_manager = EvaluationManager.create(self.training_manager.model, self.model_name, self.dataset)
        
        evaluation = self.evaluation_manager.evaluate()
        
        result = TrainingResult(self.model_name, evaluation["metrics"], evaluation["matrix"])
        
        self.report_manager.generate_metrics(result, np.unique(self.dataset.y_test).tolist(), training_duration)
        
        self.logger.info(
            message="Fin de l'évaluation", 
            logger=self.__class__.__name__, 
            run_id=self.run_id, 
            context={"model_name":self.model_name})
        
        model_id = (f"{self.model_name}_{self.run_id}")
        
        self.logger.info(
            message="Persitance du modèle", 
            logger=self.__class__.__name__, 
            run_id=self.run_id, 
            context={"model_id":model_id})
        
        self.persistence_manager.save(self.training_manager.model, model_id)
        
        