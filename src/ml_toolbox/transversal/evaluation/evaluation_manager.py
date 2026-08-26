# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from typing import Any

from config.config_manager import ConfigManager
from src.ml_toolbox.data_science.data.dataset.dataset import Dataset
from src.ml_toolbox.transversal.evaluation.evaluation_backend import (
    EvaluationBackend,
)
from src.utils.imports_utils import ImportsUtils


class EvaluationManager:
    """
    Gestionnaire d'évaluation d'un modèle.

    Cette classe orchestre l'évaluation d'un modèle entraîné.
    Le chargement du modèle est délégué à la brique persistence.

    Le backend d'évaluation masque l'implémentation technique
    utilisée par la bibliothèque ML.
    """

    @classmethod
    def create(
        cls,
        model: Any,
        model_name: str,
        dataset: Dataset,
    ) -> "EvaluationManager":
        """
        Crée un EvaluationManager configuré.

        Parameters
        ----------
        model_name :
            Nom logique du modèle à évaluer.

        dataset :
            Dataset contenant les données de test.

        Returns
        -------
        EvaluationManager
            Gestionnaire d'évaluation configuré.
        """
        
        evaluation_config = ConfigManager(
            "config/mappings/evaluation.yaml"
        )
        
        models_config = ConfigManager(
            "config/mappings/models.yaml"
        )
        
        backend_name = models_config.get(
            f"models.{model_name}.backend"
        )

        backend_module = evaluation_config.get(
            f"{backend_name}.module"
        )

        backend_class_name = evaluation_config.get(
            f"{backend_name}.class"
        )

        backend_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )

        return cls(
            backend=backend_class(model=model, dataset=dataset)
        )

    def __init__(
        self,
        backend: EvaluationBackend,
    ) -> None:
        """
        Initialise le gestionnaire d'évaluation.

        Parameters
        ----------
        backend :
            Implémentation concrète du moteur d'évaluation.
        """

        self.backend = backend

    def evaluate(
        self,
    ) -> dict[str, Any]:
        """
        Lance l'évaluation du modèle.

        Returns
        -------
        dict
            Résultats des métriques calculées.
        """

        return self.backend.evaluate()