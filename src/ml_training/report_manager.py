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
    Conteneur des résultats d'une recherche de modèle.

    Cette classe stocke les informations produites lors d'une phase de
    recherche d'hyperparamètres.

    Les données stockées permettent l'analyse et la comparaison des modèles
    via des outils d'aide à la décision (DecisionHelper).

    Ce composant ne réalise pas :
    
    - la sélection finale du modèle ;
    - l'interprétation des résultats ;
    - le déploiement du modèle.

    Attributes
    ----------
    dataset_name : str
        Nom du dataset utilisé pour l'entraînement.

    model_name : str
        Nom du modèle évalué.

    best_params : dict
        Hyperparamètres ayant obtenu le meilleur résultat pendant la recherche.

    cv_score : float
        Score obtenu par validation croisée avec le critère d'évaluation utilisé
        lors de la recherche.

    metrics : dict
        Métriques calculées sur le jeu de test.

    matrix : Any
        Matrice de confusion associée aux prédictions du meilleur estimateur.

    best_estimator : Any
        Instance du modèle entraîné avec les meilleurs paramètres trouvés.

    scoring : str
        Critère d'évaluation utilisé pendant la recherche.
    """

    dataset_name: str
    model_name: str
    best_params: dict
    cv_score: float
    metrics: dict
    matrix: Any
    best_estimator: Any
    scoring: str
    
@dataclass(slots=True)
class TrainingResult:
    """
    Conteneur des résultats d'entraînement d'un modèle.

    Cette classe représente le résultat d'un entraînement final ou isolé.
    Elle contient les informations nécessaires pour générer des rapports
    d'évaluation et alimenter les outils d'analyse.

    Attributes
    ----------
    model_name : str
        Nom du modèle entraîné.

    metrics : dict
        Ensemble des métriques calculées sur le jeu de test.

    matrix : Any
        Matrice de confusion obtenue lors de l'évaluation du modèle.
    """
    
    model_name : str
    metrics: dict
    matrix: Any

class ReportManager:
    """
    Gestionnaire de génération des rapports d'évaluation.

    Cette classe transforme les résultats d'entraînement en fichiers
    exploitables par les outils d'analyse du framework.

    Responsabilités
    ----------------
    - structurer les résultats d'entraînement ;
    - exporter les métriques au format CSV ;
    - sauvegarder les matrices de confusion ;
    - fournir une représentation persistante des performances modèles.

    Cette classe ne gère pas :

    - l'entraînement des modèles ;
    - la recherche d'hyperparamètres ;
    - la comparaison ou la sélection du modèle final ;
    - le suivi MLOps.

    L'analyse des résultats et l'aide à la décision sont réalisées par
    les composants dédiés comme DecisionHelper.
    """

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_metrics(self, 
                         results: TrainingResult | List[SearchTrainingResult], 
                         labels: list[str],
                         training_date: str | None) -> Path:
        """
        Génère un rapport contenant les résultats d'évaluation des modèles.

        Le contenu du rapport dépend du type de résultat fourni :

        - TrainingResult :
            Génération d'un rapport pour un modèle entraîné.

        - SearchTrainingResult :
            Génération d'un rapport comparatif contenant les résultats de
            recherche d'hyperparamètres pour plusieurs modèles.

        Les métriques générées sont destinées à être consultées par des outils
        d'analyse et d'aide à la décision.

        Parameters
        ----------
        results : TrainingResult | list[SearchTrainingResult]
            Résultat(s) d'entraînement à exporter.

        labels : list[str]
            Classes utilisées pour annoter les matrices de confusion.

        training_date : str | None
            Identifiant temporel utilisé pour nommer les fichiers générés.

        Returns
        -------
        Path
            Chemin du répertoire contenant le rapport généré.
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
                        "cv_score": r.cv_score,
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
        Sauvegarde une matrice de confusion au format JSON.

        La matrice sauvegardée permet une visualisation ultérieure dans les
        outils d'analyse du framework.

        Parameters
        ----------
        label : str
            Identifiant associé au modèle ou à l'expérience.

        classes : list[str]
            Liste des classes du problème de classification.

        matrix : Any
            Matrice de confusion calculée lors de l'évaluation.

        directory : str
            Sous-répertoire de stockage.

        training_date : str | None
            Date ou identifiant temporel utilisé dans le nom du fichier.

        Returns
        -------
        Path
            Chemin du fichier JSON généré.
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
        Calcule les métriques d'évaluation d'un modèle de classification.

        Les métriques calculées permettent d'analyser les performances d'un
        modèle après entraînement.

        Parameters
        ----------
        y_true : array-like
            Valeurs réelles du jeu de test.

        y_pred : array-like
            Valeurs prédites par le modèle.

        Returns
        -------
        dict
            Dictionnaire contenant les métriques calculées :
            
            - accuracy ;
            - precision ;
            - recall ;
            - f1 ;
            - f1_macro.
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