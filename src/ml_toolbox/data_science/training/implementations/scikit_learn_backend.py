# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import sys
from pathlib import Path
from typing import Any

from src.ml_toolbox.data_science.training.training_backend import TrainingBackend

sys.path.append(
    str(Path(__file__).resolve().parents[3])
)

from src.ml_toolbox.data_science.data.dataset.dataset import Dataset


class SklearnTrainingBackend(TrainingBackend):
    """
    Implémentation du TrainingManager pour Scikit-learn.
    """
    
    def __init__(
        self,
        model: Any,
        dataset: Dataset
    ) -> None:
        """
        Initialise le backend Scikit-learn.

        Parameters
        ----------
        **training_parameters :
            Paramètres transmis à la méthode
            ``fit`` lorsque ceux-ci sont supportés.
        """
        
        self.model = model
        self.dataset = dataset

    def train(
        self,
    ):
        """
        Entraîne un modèle Scikit-learn.
        """

        self.model.fit(
            self.dataset.x_train,
            self.dataset.y_train
        )

