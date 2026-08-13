# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, List
from matplotlib import pyplot as plt
import pandas as pd
import json

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from config.config_manager import ConfigManager

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
    best_fit_time: float
    
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

    def __init__(self, run_id: str, mode: str = "training") -> None:
        config = ConfigManager(
            "config/paths.yaml"
        )
        if mode == "training":
            self.reports_path = Path(config.get("project.root_folder")) / config.get("reports.root_folder") / config.get("reports.training")
        elif mode == "search":
            self.reports_path = Path(config.get("project.root_folder")) / config.get("reports.root_folder") / config.get("reports.search")
            
        self.reports_run_path = self.reports_path / run_id
        self.reports_run_path.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.mode = mode

    def generate_metrics(self, 
                         results: TrainingResult | List[SearchTrainingResult], 
                         labels: list[str],
                         duration: float = 0) -> Path:
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
        
        if self.mode == "search" and isinstance(results, List):
            
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
                        "f1_score": r.metrics["f1_score"],
                        "best_params": r.best_params,
                        "best_fit_time": r.best_fit_time
                    }
                )
                
                self.generate_confusion_matrix(f"{r.model_name}_{r.scoring}", labels, r.matrix)

            df = pd.DataFrame(rows)

            df.to_csv(self.reports_run_path / f"report.csv", index=False)
            
        elif self.mode == "training" and isinstance(results, TrainingResult):
            
            rows = [{
                    "model": results.model_name,
                    "accuracy": results.metrics["accuracy"],
                    "precision": results.metrics["precision"],
                    "recall": results.metrics["recall"],
                    "f1_score": results.metrics["f1_score"],
                    }]
            
            matrix_file = self.generate_confusion_matrix(results.model_name, labels, results.matrix)
            
            df = pd.DataFrame(rows)

            df.to_csv(self.reports_run_path / f"report.csv", index=False)
            
            metadata =     {
                "run_id": self.run_id,
                "run_type": "training",
                "created_at": self.run_id[11:],
                "duration": duration,
                "report_file": str(self.reports_run_path / f"report.csv"),
                "confusion_matrix_file": str(matrix_file)
            }

            self.generate_metadata(self.reports_run_path, metadata=metadata)
            
            registry_data = {
                "run_id": self.run_id
            }
            
            self.generate_registry(registry_data)
            
            self.update_runs_registry(registry_data)

        return self.reports_run_path
    
    def generate_confusion_matrix(
        self,
        label: str,
        classes: list[str],
        matrix: Any
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

        file_path = (
            self.reports_run_path
                / "confusion_matrix"
                / f"{label}_confusion_matrix.json"
            )
        
        (self.reports_run_path / "confusion_matrix").mkdir(parents=True, exist_ok=True)

        # Enregistrement de la matrice de confusion en json
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
            
        # Enregistrement de la matrice de confusion en format image pour le tracking
        file_path = (
            self.reports_run_path
            / "artifacts"
            / f"{label}_confusion_matrix.png"
        )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix,
            display_labels=classes,
        )

        display.plot()

        display.figure_.savefig(
            file_path,
            bbox_inches="tight",
            dpi=300,
        )

        plt.close(
            display.figure_
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
            - f1_score ;
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
            "f1_score": f1_score(
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
        
    def generate_metadata(
        self,
        metadata_path: Path, 
        metadata: dict,
    ) -> None:
        """
        Génère le fichier metadata.json associé à l'expérience.

        Parameters
        ----------
        metadata : dict
            Informations complémentaires de traçabilité
            de l'expérience.
        """

        metadata_file = (
            metadata_path
            / "metadata.json"
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )
            
    def generate_registry(
            self,
            registry_data: dict,
        ) -> None:
            """
            Génère le fichier run_registry.json associé à l'expérience.
    
            Parameters
            ----------
            data : dict
                Informations complémentaires de suivi
                de l'expérience.
            """
    
            registry_file = (
                self.reports_run_path
                / "run_registry.json"
            )
    
            with open(
                registry_file,
                "w",
                encoding="utf-8",
            ) as file:
    
                json.dump(
                    registry_data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
                
    def update_runs_registry(
            self,
            registry_data: dict,
        ) -> None:
        """
        Met à jour le registre global des expériences.

        Si le fichier runs_registry.json n'existe pas,
        il est créé avec la nouvelle expérience.

        Si le fichier existe, la nouvelle expérience est ajoutée
        à la liste des expériences. Si une expérience possédant
        le même identifiant existe déjà, ses informations sont
        mises à jour afin d'éviter les doublons.

        Parameters
        ----------
        run_data : dict
            Informations de suivi de l'expérience.
            Exemple :
            {
                "run_id": "run_20260728_145612",
                "training_status": "Done"
            }
        """

        registry_path = self.reports_path / "runs_registry.json"

        # Création du registre s'il n'existe pas
        if registry_path.exists():
            with open(registry_path, "r", encoding="utf-8") as file:
                registry = json.load(file)
        else:
            registry = {"runs": []}


        runs = registry.get("runs", [])
        
        run_id = registry_data.get("run_id")

        # Recherche d'une expérience existante
        existing_run = next(
            (
                run
                for run in runs
                if run.get("run_id") == run_id
            ),
            None,
        )

        if existing_run:
            # Mise à jour des informations existantes
            existing_run.update(registry_data)
        else:
            # Ajout d'une nouvelle expérience
            runs.append(registry_data)

        registry["runs"] = runs

        with open(registry_path, "w", encoding="utf-8") as file:
            json.dump(
                registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def update_run_info(
        self,
        info_name: str,
        info_value: str,
    ) -> None:
        """
        Ajoute/modifie une information du run.

        L'info est ajoutée dans le registre local de l'expérience
        ainsi que dans le registre global des expériences.

        Parameters
        ----------
        run_id : str
            Identifiant de l'expérience.

        info_name : str
            Nom de l"information à ajouter.
            Exemple :
            "training_status", "tracking_status", "tracking_message"

        info_value : str
            Valeur de l'information.
            Exemple :
            "Done", "Failed", "exception message"
        """

        # -------------------------
        # Mise à jour du registry local
        # -------------------------

        local_registry_path = (
            self.reports_run_path
            / "run_registry.json"
        )

        with open(local_registry_path, "r", encoding="utf-8") as file:
            local_registry = json.load(file)

        local_registry[info_name] = info_value

        with open(local_registry_path, "w", encoding="utf-8") as file:
            json.dump(
                local_registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

        # -------------------------
        # Mise à jour du registry global
        # -------------------------

        global_registry_path = (
            self.reports_path
            / "runs_registry.json"
        )

        with open(global_registry_path, "r", encoding="utf-8") as file:
            global_registry = json.load(file)

        runs = global_registry.get("runs", [])

        for run in runs:
            if run.get("run_id") == self.run_id:
                run[info_name] = info_value
                break

        with open(global_registry_path, "w", encoding="utf-8") as file:
            json.dump(
                global_registry,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def get_runs_registry(
            self
        ) -> dict:
            """
            Récupère les informations de suivi d'une expérience.

            La méthode lit le registre global de l'expérience
            et retourne son contenu sous forme de dictionnaire.

            Parameters
            ----------

            Returns
            -------
            dict
                Informations associées à l'expérience.

            Raises
            ------
            FileNotFoundError
                Si le registre global de l'expérience n'existe pas.
            """

            run_path = (
                self.reports_path
                / "runs_registry.json"
            )

            if not run_path.exists():
                raise FileNotFoundError(
                    f"Le registre de l'expérience '{self.run_id}' "
                    f"est introuvable : {run_path}"
                )

            with open(
                run_path,
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

    def get_run_registry(
        self
    ) -> dict:
        """
        Récupère les informations de suivi dun run.

        La méthode lit le registre local associé au run
        et retourne son contenu sous forme de dictionnaire.

        Parameters
        ----------
        run_id : str
            Identifiant du run.

        Returns
        -------
        dict
            Informations associées à l'expérience.

        Raises
        ------
        FileNotFoundError
            Si le registre local de l'expérience n'existe pas.
        """

        run_path = (
            self.reports_path
            / self.run_id
            / "run_registry.json"
        )

        if not run_path.exists():
            raise FileNotFoundError(
                f"Le registre de l'expérience '{self.run_id}' "
                f"est introuvable : {run_path}"
            )

        with open(
            run_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)
        
    def get_run_report(
            self
        ) -> dict:
            """
            Récupère les données d'une expérience.
    
            La méthode lit le report.csv local associé à l'expérience
            et retourne son contenu sous forme de dictionnaire.
    
            Parameters
            ----------
            run_id : str
                Identifiant de l'expérience recherchée.
    
            Returns
            -------
            dict
                Informations associées à l'expérience.
    
            Raises
            ------
            FileNotFoundError
                Si le fichier report.csv local de l'expérience n'existe pas.
            """
    
            run_path = (
                self.reports_path
                / self.run_id
            )
    
            if not run_path.exists():
                raise FileNotFoundError(
                    f"Le registre de l'expérience '{self.run_id}' "
                    f"est introuvable : {run_path}"
                )
    
            report = pd.read_csv(run_path / "report.csv")
                
            report_dict: dict[str, float] = {
                str(key): float(value)
                for key, value in (
                    report.drop(columns=["model"]).iloc[0].items()
                    )
                }
            return report_dict