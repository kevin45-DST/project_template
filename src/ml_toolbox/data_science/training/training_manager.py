# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from typing import Any

from config.config_manager import ConfigManager
from src.ml_toolbox.data_science.data.dataset.dataset import Dataset
from src.ml_toolbox.data_science.training.training_backend import TrainingBackend
from src.ml_toolbox.data_science.training.training_router import TrainingRouter
from src.utils.imports_utils import ImportsUtils


class TrainingManager:

    """
    Gestionnaire de l'entrainement indépendant du backend utilisé.

    Cette classe fournit les outils nécessaires pour gérer
    l'entrainement.

    Le backend utilisé est injecté afin de masquer
    l'implémentation technique (Scikit-learn, PyTorch, etc...).
    """

    @classmethod
    def create(
        cls,
        model_name: str,
        dataset: Dataset,
        **kwargs
    ) -> "TrainingManager":
        """
        Crée un TrainingManager configuré.

        Parameters
        ----------
        model_name :
            Nom logique du modèle à entraîner.

        Returns
        -------
        TrainingManager
            Gestionnaire d'entraînement configuré.
        """

        router = TrainingRouter()

        router_resolution = router.resolve(
            model_name=model_name,
        )
        
        model = router_resolution["model"]
        
        backend_name = router_resolution["backend_name"]

        training_config = ConfigManager(
            "config/mappings/training.yaml"
        )

        backend_module = training_config.get(
            f"{backend_name}.module"
        )

        backend_class_name = training_config.get(
            f"{backend_name}.class"
        )

        backend_implementation_class = ImportsUtils.get_class(
            backend_module,
            backend_class_name,
        )

        backend = backend_implementation_class(model=model, dataset=dataset)

        return cls(
            model=model,
            dataset=dataset,
            backend=backend
        )


    def __init__(
        self,
        model: Any,
        dataset: Dataset,
        backend: TrainingBackend
        
    ) -> None:
        """
        Initialise le gestionnaire de training.

        Parameters
        ----------
        backend :
            Implémentation concrète du système de training.
        """

        self.model = model
        self.dataset = dataset
        self.backend = backend

    def train(
        self
    ):
        """
        Lance l'entraînement du modèle.
        """

        return self.backend.train()