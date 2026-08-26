# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from __future__ import annotations

import numpy as np

from src.ml_toolbox.transversal.logs.log_collector.log_collector_manager import LogCollectorManager
from src.ml_toolbox.transversal.reporting.report_manager import ReportManager, SearchTrainingResult
from src.ml_toolbox.transversal.evaluation.evaluation_manager import EvaluationManager
from src.ml_toolbox.data_science.best_model_research.strategy.gridcv_strategy import GridCVStrategy

from src.ml_toolbox.data_science.data.dataset.dataset import Dataset
from src.utils.ids_utils import runId
    
class SearchPipeline:
    """
    Pipeline de recherche et d'évaluation de modèles.

    Cette classe orchestre la recherche d'hyperparamètres pour les modèles
    configurés, puis évalue chaque meilleur candidat sur le jeu de test.

    Pour chaque modèle :

    1. une stratégie de recherche est exécutée ;
    2. le meilleur modèle obtenu est évalué ;
    3. les résultats sont stockés dans un ``SearchTrainingResult``.

    À la fin de la recherche, l'ensemble des résultats est persisté dans
    un rapport associé à un run unique.

    Le pipeline ne sélectionne pas lui-même un modèle final parmi les
    différents candidats.
    """
    
    # ==================================================
    # Configuration de la recherche
    # ==================================================

    strategy = GridCVStrategy

    model_parameters = {
        "logistic_regression": {
            "C": [0.1, 1.0, 10.0],
        },
        "random_forest_classifier": {
            "n_estimators": [100, 200, 500],
            "max_depth": [None, 10, 20],
        },
        "xgboost_classifier": {
            "n_estimators": [100, 200],
            "max_depth": [3, 6, 10],
        },
    }

    scoring = "f1"
    cv = 5
    n_jobs = -1

    def __init__(self, dataset: Dataset) -> None:
        """
        Initialise un nouveau run de recherche.

        Parameters
        ----------
        dataset : Dataset
            Dataset utilisé pour la recherche et l'évaluation des modèles.
        """
        self.dataset = dataset
        
        self.run_id = runId.create()
        
        self.report_manager = ReportManager(run_id = self.run_id, mode="search")
        
        self.logger = LogCollectorManager()

    def run(self) -> None:
        """
        Exécute la recherche du meilleur modèle.

        La stratégie sélectionnée est utilisée pour effectuer la recherche
        à partir des modèles et paramètres définis dans la configuration
        du pipeline.

        Le candidat obtenu est ensuite évalué sur le jeu de test et les
        résultats sont enregistrés dans le rapport.

        Les étapes sont communes à toutes les stratégies :

        1. Exécution de la stratégie de recherche.
        2. Évaluation du meilleur candidat.
        3. Génération du rapport.

        La stratégie est responsable de la méthode utilisée pour rechercher
        le meilleur modèle, mais ne gère ni l'évaluation finale ni le
        reporting.
        """
        
        results = []
        
        self.logger.debug(message="Début du run", logger=self.__class__.__name__, run_id=self.run_id)
        
        for model_name, param_grid in self.model_parameters.items():
            
            self.logger.debug(
                message=f"Début du search model {model_name}", 
                logger=self.__class__.__name__, 
                run_id=self.run_id, 
                context={"param_grid":param_grid}
                )
            
            search_strategy = self.strategy(
                    model_name=model_name,
                    param_grid=param_grid,
                    scoring=self.scoring,
                    cv=self.cv,
                    n_jobs=self.n_jobs,
                )

            search_strategy.search(
                self.dataset.x_train,
                self.dataset.y_train,
            )
            
            self.logger.debug(
                message=f"Fin du search model {model_name}", 
                logger=self.__class__.__name__, 
                run_id=self.run_id, 
                )
            
            self.logger.debug(
                message=f"Début de l'évaluation model {model_name}", 
                logger=self.__class__.__name__, 
                run_id=self.run_id, 
                context={"param_grid":param_grid}
                )
            
            evaluation_manager = EvaluationManager.create(
                model=search_strategy.best_model,
                model_name=model_name,
                dataset=self.dataset,
            )

            evaluation = evaluation_manager.evaluate()
                      
            search_result = SearchTrainingResult(
                            best_params=search_strategy.best_params,
                            scoring=self.scoring,
                            best_estimator=search_strategy.best_model,
                            cv_score=search_strategy.best_score,
                            dataset_name=self.dataset.name,
                            matrix=evaluation["matrix"],
                            metrics=evaluation["metrics"],
                            model_name=model_name,
                            best_fit_time=search_strategy.best_fit_time
            )
            
            results.append(search_result)
            
            self.logger.debug(
                message=f"Fin de l'évaluation model {model_name}", 
                logger=self.__class__.__name__, 
                run_id=self.run_id, 
                )
            
        self.report_manager.generate_metrics(results, np.unique(self.dataset.y_test).tolist())
        
        self.logger.debug(message="Fin du run", logger=self.__class__.__name__, run_id=self.run_id)