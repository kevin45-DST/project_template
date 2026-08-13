# Copyright © 2026 Kévin DELANOUE

# License: see LICENSE

from typing import Any

from src.ml_toolbox.data_science.data.dataset.dataset import Dataset
from src.ml_toolbox.data_science.training.training_backend import TrainingBackend


class XGBoostTrainingBackend(TrainingBackend):
    """
    Implémentation du TrainingBackend pour XGBoost.
    """

    def __init__(
        self,
        model: Any,
        dataset: Dataset,
    ) -> None:
        """
        Initialise le backend XGBoost.

        Parameters
        ----------
        model : Any
            Modèle XGBoost à entraîner.

        dataset : Dataset
            Dataset utilisé pour l'entraînement.
        """

        self.model = model
        self.dataset = dataset

    def train(
        self,
    ):
        """
        Entraîne un modèle XGBoost.

        Le modèle entraîné est conservé dans l'attribut ``model``.
        """

        self.model.fit(
            self.dataset.x_train,
            self.dataset.y_train,
        )