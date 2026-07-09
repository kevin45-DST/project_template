from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, List
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

@dataclass(slots=True)
class SearchTrainingResult:
    """
    Résultat d'un entraînement de modèle lors de la recherche du meilleur modèle.

    Attributes
    ----------
    dataset_name : str
    model_name : str
    best_params : dict
    best_score : float
    metrics : dict
    matrix: Any
    best_estimator : Any
    scoring: str
    """

    dataset_name: str
    model_name: str
    best_params: dict
    best_score: float
    metrics: dict
    matrix: Any
    best_estimator: Any
    scoring: str
    
@dataclass(slots=True)
class TrainingResult:
    """
    Résultat d'un entraînement de modèle.

    Attributes
    ----------
    model_name : str
    metrics : dict
    matrix: Any
    """
    
    model_name : str
    metrics: dict
    matrix: Any

class ReportManager:
    """
    Générateur de rapports d'entraînement.

    Cette classe transforme les résultats d'entraînement en fichier CSV.

    Responsabilités
    ----------------
    - conversion des résultats en DataFrame
    - export CSV
    - structuration des performances

    Elle ne gère PAS :
    - l'entraînement
    - la sélection de modèles
    - la sauvegarde de modèles

    Comment utiliser
    ----------------
    >>> reporter = ReportManager("reports")
    >>> reporter.generate(results)
    """

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_metrics(self, 
                         results: TrainingResult | List[SearchTrainingResult], 
                         labels: list[str],
                         training_date: str | None) -> Path:
        """
        Génère un rapport CSV.

        Parameters
        ----------
        results : List[TrainingResult]

        Returns
        -------
        Path
            Chemin du fichier généré.
        """

        rows = []
        directory = ""
        
        if isinstance(results, List):
            file_path = self.output_path / directory
            file_path.mkdir(parents=True, exist_ok=True)
            (file_path / "confusion_matrix").mkdir(parents=True, exist_ok=True)
            
            for r in results:
                rows.append(
                    {
                        "label": f"{r.model_name}_{r.scoring}", 
                        "model": r.model_name,
                        "scoring": r.scoring,
                        "best_score": r.best_score,
                        "accuracy": r.metrics["accuracy"],
                        "precision": r.metrics["precision"],
                        "recall": r.metrics["recall"],
                        "f1": r.metrics["f1"],
                        "best_params": r.best_params,
                    }
                )
                
                self.generate_confusion_matrix(f"{r.model_name}_{r.scoring}", labels, r.matrix, directory, None)

            df = pd.DataFrame(rows)

            df.to_csv(file_path / f"report.csv", index=False)
        else:
            file_path = self.output_path / directory
            file_path.mkdir(parents=True, exist_ok=True)
            
            rows = [{
                    "model": results.model_name,
                    "accuracy": results.metrics["accuracy"],
                    "precision": results.metrics["precision"],
                    "recall": results.metrics["recall"],
                    "f1": results.metrics["f1"],
                    }]
            
            self.generate_confusion_matrix(results.model_name, labels, results.matrix, directory, training_date)
            
            df = pd.DataFrame(rows)

            df.to_csv(file_path / f"report_{training_date}.csv", index=False)

        return file_path
    
    def generate_confusion_matrix(
        self,
        label: str,
        classes: list[str],
        matrix: Any,
        directory: str,
        training_date: str | None
    ) -> Path:
        """
        Sauvegarde une matrice de confusion associée à un modèle.

        Parameters
        ----------
        label : str
            Identifiant unique du modèle ou de l'expérience.

        y_true : array-like
            Valeurs réelles.

        y_pred : array-like
            Prédictions du modèle.

        Returns
        -------
        Path
            Chemin du fichier généré.
        """

        data = {
            "classes": classes,
            "matrix": matrix.tolist(),
        }

        if training_date:
            file_path = (
                self.output_path
                / directory
                / f"{label}_{training_date}_confusion_matrix.json"
            )
        else:
            file_path = (
                self.output_path
                / directory
                / "confusion_matrix"
                / f"{label}_confusion_matrix.json"
            )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

        return file_path
    
    @staticmethod
    def compute_metrics(
        y_true,
        y_pred,
    ) -> dict:
        """
        Calcule les principales métriques de classification.

        Parameters
        ----------
        y_true : array-like
            Labels réels.

        y_pred : array-like
            Labels prédits.

        Returns
        -------
        dict
            Dictionnaire contenant les métriques.
        """

        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true,
                y_pred,
                average="binary",
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                average="binary",
                zero_division=0,
            ),
            "f1": f1_score(
                y_true,
                y_pred,
                average="binary",
                zero_division=0,
            ),
            "f1_macro": f1_score(
                y_true,
                y_pred,
                average="macro",
                zero_division=0,
            ),
        }