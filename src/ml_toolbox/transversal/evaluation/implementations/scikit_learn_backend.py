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
    Implémentation de l'évaluation pour Scikit-learn.
    """

    def __init__(
        self,
        model: Any,
        dataset,
    ) -> None:

        self.model = model
        self.dataset = dataset


    def evaluate(
        self,
    ) -> dict:

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