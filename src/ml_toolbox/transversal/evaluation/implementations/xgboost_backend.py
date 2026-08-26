# Copyright © 2026 Kévin DELANOUE

# License: see LICENSE

from typing import Any

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from src.ml_toolbox.transversal.evaluation.evaluation_backend import (
    EvaluationBackend,
)


class XGBoostEvaluationBackend(EvaluationBackend):
    """
    Implémentation de l'évaluation pour XGBoost.

    Ce backend utilise les prédictions du modèle XGBoost entraîné pour
    calculer les métriques de classification et la matrice de confusion.

    Parameters
    ----------
    model : Any
        Modèle XGBoost entraîné.

    dataset : Dataset
        Dataset contenant les données de test utilisées pour l'évaluation.
    """

    def __init__(
        self,
        model: Any,
        dataset,
    ) -> None:
        """
        Initialise le backend d'évaluation XGBoost.

        Parameters
        ----------
        model : Any
            Modèle XGBoost entraîné.

        dataset : Dataset
            Dataset contenant les données de test.
        """

        self.model = model
        self.dataset = dataset

    def evaluate(
        self,
    ) -> dict:
        """
        Évalue le modèle XGBoost sur le jeu de test.

        Returns
        -------
        dict
            Dictionnaire contenant les métriques de classification et
            la matrice de confusion.
        """

        y_pred = self.model.predict(
            self.dataset.x_test
        )

        metrics = {
            "accuracy": accuracy_score(
                self.dataset.y_test,
                y_pred,
            ),
            "precision": precision_score(
                self.dataset.y_test,
                y_pred,
            ),
            "recall": recall_score(
                self.dataset.y_test,
                y_pred,
            ),
            "f1_score": f1_score(
                self.dataset.y_test,
                y_pred,
            ),
        }

        matrix = confusion_matrix(
            self.dataset.y_test,
            y_pred,
        )

        return {
            "metrics": metrics,
            "matrix": matrix,
        }