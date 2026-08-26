# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from typing import Any

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

from src.ml_toolbox.transversal.evaluation.evaluation_backend import (
    EvaluationBackend,
)


class SklearnEvaluationBackend(
    EvaluationBackend
):
    """
    Backend d'évaluation utilisant Scikit-learn.

    Cette classe utilise l'API de prédiction du modèle ainsi que les
    fonctions d'évaluation de Scikit-learn pour calculer les métriques
    de classification et la matrice de confusion.

    Parameters
    ----------
    model : Any
        Modèle entraîné compatible avec l'API de prédiction de
        Scikit-learn.

    dataset : Dataset
        Dataset contenant les données de test utilisées pour l'évaluation.
    """

    def __init__(
        self,
        model: Any,
        dataset,
    ) -> None:
        """
        Initialise le backend d'évaluation.

        Parameters
        ----------
        model : Any
            Modèle entraîné à évaluer.

        dataset : Dataset
            Dataset contenant les données de test.
        """
        self.model = model
        self.dataset = dataset


    def evaluate(
        self,
    ) -> dict:
        """
        Évalue le modèle sur le jeu de test.

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
            "matrix": matrix
            }