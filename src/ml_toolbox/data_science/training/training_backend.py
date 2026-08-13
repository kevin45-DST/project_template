# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from abc import ABC, abstractmethod
from typing import Any

from src.ml_toolbox.data_science.data.dataset.dataset import Dataset


class TrainingBackend(ABC):
    """
    Interface définissant les opérations d'entraînement d'un modèle.

    Les implémentations concrètes sont responsables de l'utilisation
    de la bibliothèque de Machine Learning (Scikit-learn, TensorFlow,
    PyTorch, etc.).
    """
    
    def __init__(
        self,
        model: Any,
        dataset: Dataset,
    ) -> None:
        """
        Initialise le backend d'entraînement.

        Parameters
        ----------
        model :
            Modèle à entraîner.

        dataset :
            Dataset utilisé pour l'entraînement et l'évaluation.
        """

        self.model = model
        self.dataset = dataset

    @abstractmethod
    def train(
        self
    ):
        """
        Entraîne un modèle.

        Parameters
        ----------
        Self : Tous les éléments necessaires sont passés dans le constructeur

        Returns
        -------
        Modèle entraîné dans le self.
        """
        pass